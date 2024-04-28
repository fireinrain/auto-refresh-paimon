import cfips
import checker
import config
import database
import utils


def main():
    # get cloudflare cdn proxy from db
    vless_nodes = database.session.query(database.V2ServerVless).filter_by(tls=True).all()
    vless_nodes = [n for n in vless_nodes if n.port != n.server_port]

    ip_provider = cfips.AAAGroupIPProvider()
    ips = ip_provider.get_ips()
    if not ips:
        print(">>> 当前没有可用的Cloudflare IP")
        return
    country_map = config.GlobalConfig.get_node_country_map()
    has_use = set()

    for node in vless_nodes:
        print(f">>> 当前节点: {node.name}")
        port_open = checker.IPChecker.check_port_open(node.host, node.port, 3, 1)
        if not port_open:
            print(f">>> 当前优选IP端口已失效: {node.host}:{node.port},更新中...")
            selected_ip = None
            for ip in ips:
                use_index = ip.ip+str(ip.port)+str(ip.tls)
                country_by_keyword = utils.detect_country_by_keyword(country_map, node.name)
                if ip.country in country_by_keyword and use_index not in has_use:
                    has_use.add(ip.ip + str(ip.port) + str(ip.tls))
                    selected_ip = ip
                    break
            if not selected_ip:
                print(f">>> 无法找到适合当前地区的IP: {node.name}: {selected_ip},不做更新")
                print("--------------------------------------------------------")
                continue
            print(f">>> 已找到适合当前地区的IP：{node.name}: {selected_ip}")
            node.host = selected_ip.ip
            node.port = selected_ip.port
            try:
                database.session.commit()
                print(f">>> Update node ip and port successfully!")
            except Exception as e:
                print(f">>> Error update node info: {e}")
                database.session.rollback()
        else:
            print(f">>> 当前优选IP端口未失效: {node.host}:{node.port},不做更新处理")
        print("--------------------------------------------------------")


if __name__ == '__main__':
    print(f"Welcome to auto-refresh-paimon cloud!")
    # proxy = checker.IPChecker.check_cloudflare_proxy("104.19.32.25", "443", True)
    # print(proxy)
    main()
