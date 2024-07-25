import asyncio
import random
import sys

import cfips
import checker
import config
import database
import notify
import utils


async def schedule_conn_check():
    db = next(database.get_db())
    # get cloudflare cdn proxy from db
    vless_nodes = db.query(database.V2ServerVless).filter_by(tls=True).all()
    vless_nodes = [n for n in vless_nodes if n.port != n.server_port]

    ip_provider = cfips.AAAGroupIPProvider()
    ips = ip_provider.get_ips()

    # 欢乐时光 和 其他免费订阅链接
    cf_sublinks_ip_provider = cfips.SharedCFSublinksIPProvider()
    shared_ips = cf_sublinks_ip_provider.get_ips()
    ips.extend(shared_ips)

    # open port
    redis_provider = cfips.OpenPortSnifferRedisProvider()
    provider_get_ips = redis_provider.get_ips()
    ips.extend(provider_get_ips)

    # IPDB github 的数据
    cfip_provider = cfips.IpdbBestCFIPProvider()
    ipdb_ips = cfip_provider.get_ips()
    ips.extend(ipdb_ips)

    if not ips:
        print(">>> 当前没有可用的Cloudflare IP")
        return
    country_map = config.GlobalConfig.get_node_country_map()

    print(f">>> 检查VLESS节点: {len(vless_nodes)}...")
    for node in vless_nodes:
        has_use = set()
        print(f">>> 当前节点: {node.name}")
        if "续订" in node.name:
            continue
        if "节点" in node.name:
            continue
        if "初次" in node.name:
            continue
        port_open = checker.IPChecker.check_port_open_with_retry(node.host, node.port, 10)
        if not port_open:
            print(f">>> 当前优选IP端口已失效: {node.host}:{node.port},更新中...")
            selected_ips = []
            for ip in ips:
                use_index = ip.ip + str(ip.port) + str(ip.tls)
                country_by_keyword = utils.detect_country_by_keyword(country_map, node.name)
                if ip.country in country_by_keyword and use_index not in has_use:
                    has_use.add(ip.ip + str(ip.port) + str(ip.tls))
                    selected_ips.append(ip)
            if not selected_ips:
                print(f">>> 无法找到适合当前地区的IP: {node.name}: {selected_ips},不做更新")
                print(f">>> 考虑到可用性, 使用US地区IP代替,进行更新")
                for ip in ips:
                    use_index = ip.ip + str(ip.port) + str(ip.tls)
                    country_by_keyword = utils.detect_country_by_keyword(country_map, "美国节点,美国专线")
                    if ip.country in country_by_keyword and use_index not in has_use:
                        has_use.add(ip.ip + str(ip.port) + str(ip.tls))
                        selected_ips.append(ip)
                print("--------------------------------------------------------")
            selected_ip = random.choice(selected_ips)
            print(f">>> 已找到适合当前地区的IP：{node.name}: {selected_ip}")
            # TODO 再使用前检测是否在线  在线检测是否是cf反代
            # 目前默认都是可用的 这个应该会存在误差
            db.is_active
            temp_host = node.host
            temp_port = node.port
            temp_node_name = node.name
            node.host = selected_ip.ip
            node.port = selected_ip.port
            try:
                db.commit()
                print(f">>> Update node ip and port successfully!")
                # 推送消息
                telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
                                                                "auto-refresh-paimon paimon-cloud",
                                                                f"{temp_node_name} {temp_host}:{temp_port} changed to {node.host}:{node.port}")
                telegram_notify = utils.clean_str_for_tg(telegram_notify)
                await notify.send_message2bot(telegram_notify)
            except Exception as e:
                print(f">>> Error update node info: {e}")
                db.rollback()
        else:
            print(f">>> 当前优选IP端口未失效: {node.host}:{node.port},不做更新处理")
        print("--------------------------------------------------------")

    trojan_nodes = db.query(database.V2ServerTrojan).filter_by(allow_insecure=False).all()
    trojan_nodes = [n for n in trojan_nodes if n.port != n.server_port]
    print(f">>> 检查TROJAN节点: {len(trojan_nodes)}...")
    for node in trojan_nodes:
        has_use = set()
        print(f">>> 当前节点: {node.name}")
        port_open = checker.IPChecker.check_port_open_with_retry(node.host, node.port, 10)
        if not port_open:
            print(f">>> 当前优选IP端口已失效: {node.host}:{node.port},更新中...")
            selected_ips = []
            for ip in ips:
                use_index = ip.ip + str(ip.port) + str(ip.tls)
                country_by_keyword = utils.detect_country_by_keyword(country_map, node.name)
                if ip.country in country_by_keyword and use_index not in has_use:
                    has_use.add(ip.ip + str(ip.port) + str(ip.tls))
                    selected_ips.append(ip)
            if not selected_ips:
                print(f">>> 无法找到适合当前地区的IP: {node.name}: {selected_ips},不做更新")
                print(f">>> 考虑到可用性, 使用US地区IP代替,进行更新")
                for ip in ips:
                    use_index = ip.ip + str(ip.port) + str(ip.tls)
                    country_by_keyword = utils.detect_country_by_keyword(country_map, "美国节点,美国专线")
                    if ip.country in country_by_keyword and use_index not in has_use:
                        has_use.add(ip.ip + str(ip.port) + str(ip.tls))
                        selected_ips.append(ip)
                print("--------------------------------------------------------")
            selected_ip = random.choice(selected_ips)
            print(f">>> 已找到适合当前地区的IP：{node.name}: {selected_ip}")
            # TODO 再使用前检测是否在线  在线检测是否是cf反代
            # 目前默认都是可用的 这个应该会存在误差
            temp_host = node.host
            temp_port = node.port
            temp_node_name = node.name
            node.host = selected_ip.ip
            node.port = selected_ip.port
            try:
                db.commit()
                print(f">>> Update node ip and port successfully!")
                # 推送消息
                telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
                                                                "auto-refresh-paimon paimon-cloud",
                                                                f"{temp_node_name} {temp_host}:{temp_port} changed to {node.host}:{node.port}")
                telegram_notify = utils.clean_str_for_tg(telegram_notify)
                await notify.send_message2bot(telegram_notify)
            except Exception as e:
                print(f">>> Error update node info: {e}")
                db.rollback()
        else:
            print(f">>> 当前优选IP端口未失效: {node.host}:{node.port},不做更新处理")
        print("--------------------------------------------------------")

    vmess_nodes = db.query(database.V2ServerVMess).filter_by(tls=True).all()
    vmess_nodes = [n for n in vmess_nodes if n.port != n.server_port]
    print(f">>> 检查VMESS节点: {len(vmess_nodes)}...")
    for node in vmess_nodes:
        has_use = set()

        print(f">>> 当前节点: {node.name}")
        port_open = checker.IPChecker.check_port_open_with_retry(node.host, node.port, 10)
        if not port_open:
            print(f">>> 当前优选IP端口已失效: {node.host}:{node.port},更新中...")
            selected_ips = []
            for ip in ips:
                use_index = ip.ip + str(ip.port) + str(ip.tls)
                country_by_keyword = utils.detect_country_by_keyword(country_map, node.name)
                if ip.country in country_by_keyword and use_index not in has_use:
                    has_use.add(ip.ip + str(ip.port) + str(ip.tls))
                    selected_ips.append(ip)
            if not selected_ips:
                print(f">>> 无法找到适合当前地区的IP: {node.name}: {selected_ips},不做更新")
                print(f">>> 考虑到可用性, 使用US地区IP代替,进行更新")
                for ip in ips:
                    use_index = ip.ip + str(ip.port) + str(ip.tls)
                    country_by_keyword = utils.detect_country_by_keyword(country_map, "美国节点,美国专线")
                    if ip.country in country_by_keyword and use_index not in has_use:
                        has_use.add(ip.ip + str(ip.port) + str(ip.tls))
                        selected_ips.append(ip)

                print("--------------------------------------------------------")
            selected_ip = random.choice(selected_ips)

            print(f">>> 已找到适合当前地区的IP：{node.name}: {selected_ip}")
            # TODO 再使用前检测是否在线  在线检测是否是cf反代
            # 目前默认都是可用的 这个应该会存在误差
            temp_host = node.host
            temp_port = node.port
            temp_node_name = node.name
            node.host = selected_ip.ip
            node.port = selected_ip.port
            try:
                db.commit()
                print(f">>> Update node ip and port successfully!")
                # 推送消息
                telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
                                                                "auto-refresh-paimon paimon-cloud",
                                                                f"{temp_node_name} {temp_host}:{temp_port} changed to {node.host}:{node.port}")
                telegram_notify = utils.clean_str_for_tg(telegram_notify)
                await notify.send_message2bot(telegram_notify)
            except Exception as e:
                print(f">>> Error update node info: {e}")
                db.rollback()
        else:
            print(f">>> 当前优选IP端口未失效: {node.host}:{node.port},不做更新处理")
        print("--------------------------------------------------------")


async def schedule_gfw_ban_check():
    db = next(database.get_db())
    vless_nodes = db.query(database.V2ServerVless).filter_by(tls=True).all()
    vless_nodes = [n for n in vless_nodes if n.port != n.server_port]
    for node in vless_nodes:
        if "续订" in node.name:
            continue
        if "节点" in node.name:
            continue
        if "初次" in node.name:
            continue
        port = node.port
        ip = node.host
        baned_with_gfw = checker.IPChecker.check_band_with_gfw_with_retry(ip, port, 3)
        print(f"Proxy id: {ip}:{port} gfwban status: {baned_with_gfw}")

        await asyncio.sleep(5)
        if not baned_with_gfw:
            continue
        temp_node_name = node.name
        temp_host = node.host
        temp_port = node.port
        try:
            node.port = 55555
            node.host = "127.0.0.1"
            db.commit()
            print(f">>> ip and port was baned by GFW,update node ip and port to fake for waiting update!")
            print(f">>> {temp_node_name} {temp_host}:{temp_port}!")

            # 推送消息
            telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
                                                            "auto-refresh-paimon paimon-cloud-gfw",
                                                            f"{temp_node_name} {temp_host}:{temp_port} changed to {node.host}:{node.port}")
            telegram_notify = utils.clean_str_for_tg(telegram_notify)
            await notify.send_message2bot(telegram_notify)
        except Exception as e:
            print(f">>> Error update node info: {e}")
            db.rollback()

        # print(f">>> ip and port was baned by GFW,update node ip and port to fake for waiting update!")
        # print(f">>> {node.name} {node.host}:{node.port}!")
        # temp_host = "127.0.0.1"
        # temp_port = 55555
        # # 推送消息
        # telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
        #                                                 "auto-refresh-paimon paimon-cloud-gfw",
        #                                                 f"{node.name} {node.name}:{node.name} changed to {temp_host}:{temp_port}")
        # telegram_notify = utils.clean_str_for_tg(telegram_notify)
        # await notify.send_message2bot(telegram_notify)
        print("--------------------------------------------------------")

    trojan_nodes = db.query(database.V2ServerTrojan).filter_by(allow_insecure=False).all()
    trojan_nodes = [n for n in trojan_nodes if n.port != n.server_port]
    for node in trojan_nodes:
        port = node.port
        ip = node.host
        baned_with_gfw = checker.IPChecker.check_band_with_gfw_with_retry(ip, port, 3)
        print(f"Proxy id: {ip}:{port} gfwban status: {baned_with_gfw}")

        await asyncio.sleep(5)
        if not baned_with_gfw:
            continue
        temp_node_name = node.name
        temp_host = node.host
        temp_port = node.port
        try:
            node.port = 55555
            node.host = "127.0.0.1"
            db.commit()
            print(f">>> ip and port was baned by GFW,update node ip and port to fake for waiting update!")
            print(f">>> {temp_node_name} {temp_host}:{temp_port}!")

            # 推送消息
            telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
                                                            "auto-refresh-paimon paimon-cloud-gfw",
                                                            f"{temp_node_name} {temp_host}:{temp_port} changed to {node.host}:{node.port}")
            telegram_notify = utils.clean_str_for_tg(telegram_notify)
            await notify.send_message2bot(telegram_notify)
        except Exception as e:
            print(f">>> Error update node info: {e}")
            db.rollback()

        # print(f">>> ip and port was baned by GFW,update node ip and port to fake for waiting update!")
        # print(f">>> {node.name} {node.host}:{node.port}!")
        # temp_host = "127.0.0.1"
        # temp_port = 55555
        # # 推送消息
        # telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
        #                                                 "auto-refresh-paimon paimon-cloud-gfw",
        #                                                 f"{node.name} {node.name}:{node.name} changed to {temp_host}:{temp_port}")
        # telegram_notify = utils.clean_str_for_tg(telegram_notify)
        # await notify.send_message2bot(telegram_notify)
        print("--------------------------------------------------------")

    vmess_nodes = db.query(database.V2ServerVMess).filter_by(tls=True).all()
    vmess_nodes = [n for n in vmess_nodes if n.port != n.server_port]
    for node in vmess_nodes:
        port = node.port
        ip = node.host
        baned_with_gfw = checker.IPChecker.check_band_with_gfw_with_retry(ip, port, 3)
        print(f"Proxy id: {ip}:{port} gfwban status: {baned_with_gfw}")
        await asyncio.sleep(5)
        if not baned_with_gfw:
            continue
        temp_node_name = node.name
        temp_host = node.host
        temp_port = node.port
        try:
            node.port = 55555
            node.host = "127.0.0.1"
            db.commit()
            print(f">>> ip and port was baned by GFW,update node ip and port to fake for waiting update!")
            print(f">>> {temp_node_name} {temp_host}:{temp_port}!")

            # 推送消息
            telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
                                                            "auto-refresh-paimon paimon-cloud-gfw",
                                                            f"{temp_node_name} {temp_host}:{temp_port} changed to {node.host}:{node.port}")
            telegram_notify = utils.clean_str_for_tg(telegram_notify)
            await notify.send_message2bot(telegram_notify)
        except Exception as e:
            print(f">>> Error update node info: {e}")
            db.rollback()

        # print(f">>> ip and port was baned by GFW,update node ip and port to fake for waiting update!")
        # print(f">>> {node.name} {node.host}:{node.port}!")
        # temp_host = "127.0.0.1"
        # temp_port = 55555
        # # 推送消息
        # telegram_notify = notify.pretty_telegram_notify("🍻🍻AutoRefreshPaimon更新",
        #                                                 "auto-refresh-paimon paimon-cloud-gfw",
        #                                                 f"{node.name} {node.name}:{node.name} changed to {temp_host}:{temp_port}")
        # telegram_notify = utils.clean_str_for_tg(telegram_notify)
        # await notify.send_message2bot(telegram_notify)
        print("--------------------------------------------------------")


async def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <argument>")
        sys.exit(1)

    argument = sys.argv[1]

    if argument == "proxy":
        await schedule_conn_check()
    elif argument == "gfwban":
        # 检测方法存在比较大的误判
        await schedule_gfw_ban_check()
    else:
        print(f"Invalid argument: {argument}")


if __name__ == '__main__':
    print(f"Welcome to auto-refresh-paimon cloud!")
    # proxy = checker.IPChecker.check_cloudflare_proxy("104.19.32.25", "443", True)
    # print(proxy)
    asyncio.run(main())

