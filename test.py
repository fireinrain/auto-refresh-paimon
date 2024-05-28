import json
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
        import subprocess
        import json

        curl_command = [
            'curl', 'https://www.vps234.com/ipcheck/getdata/',
            '-H', 'Accept: */*',
            '-H', 'Accept-Language: zh,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,ja;q=0.6',
            '-H', 'Cache-Control: no-cache',
            '-H', 'Connection: keep-alive',
            '-H', 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8',
            '-H', 'Origin: https://www.vps234.com',
            '-H', 'Pragma: no-cache',
            '-H', 'Referer: https://www.vps234.com/ipchecker/',
            '-H', 'Sec-Fetch-Dest: empty',
            '-H', 'Sec-Fetch-Mode: cors',
            '-H', 'Sec-Fetch-Site: same-origin',
            '-H',
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            '-H', 'X-Requested-With: XMLHttpRequest',
            '-H', 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            '-H', 'sec-ch-ua-mobile: ?0',
            '-H', 'sec-ch-ua-platform: "macOS"',
            '--data-raw', 'idName=itemblockid1716887992244&ip=34.150.133.11'
        ]

        # Execute the curl command
        result = subprocess.run(curl_command, capture_output=True, text=True)

        # Print the output
        print(result.stdout)
        # resp = json.loads(str(result))

        # Print the output
        # print(resp)

