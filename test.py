from unittest import TestCase

import checker


class TestIPChecker(TestCase):
    def test_check_port_open(self):
        print(checker.IPChecker.check_port_open("211.22.240.107", "30686"))

    def test_check_baned_with_gfw(self):
        print(checker.IPChecker.check_baned_with_gfw("i-love-paimon-cloud-v2.666961.xyz", "443"))

    def test_check_baned_with_gfw_v2(self):
        print(checker.IPChecker.check_baned_with_gfw_v2("34.150.133.11", 443))

    def test_check_cloudflare_proxy(self):
        proxy = checker.IPChecker.check_cloudflare_proxy("104.19.32.25", "8443", True)
        print(proxy)
        proxy2 = checker.IPChecker.check_cloudflare_proxy("61.222.202.104", "23555", True)
        print(proxy2)

    def test_check_if_cf_proxy(self):
        checkers = checker.IPChecker.check_if_cf_tls_proxy("154.17.21.196", "443")
        print(checkers)

    def test_range(self):
        i = 2
        for a in range(i):
            print(a)

    def test_key_out(self):
        a = {"a": "b"}
        print(a["f"])

    def test_curl(self):
        import requests

        url = 'https://www.vps234.com/ipcheck/getdata/'

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,ja;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.vps234.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.vps234.com/ipchecker/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        data = {
            'idName': 'itemblockid1716887992202',
            'ip': '34.150.133.11'
        }

        response = requests.post(url, headers=headers, data=data)

        print(response.text)

