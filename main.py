import checker
import database


def main():
    # get cloudflare cdn proxy from db
    vless_nodes = database.session.query(database.V2ServerVless).filter_by(tls=True).all()
    vless_nodes = [n for n in vless_nodes if n.port != n.server_port]
    for node in vless_nodes:
        print(f">>> 当前节点: {node.name}")
        port_open = checker.IPChecker.check_port_open(node.host, node.port, 2, 1)
        if not port_open:
            print(f">>> 当前优选IP端口已失效: {node.host}:{node.port},更新中...")
            node.port = '9999'
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
