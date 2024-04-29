from unittest import TestCase

import checker


class TestIPChecker(TestCase):
    def test_check_port_open(self):
        print(checker.IPChecker.check_port_open("127.0.0.1", "22"))

    def test_check_baned_with_gfw(self):
        print(checker.IPChecker.check_baned_with_gfw("220.130.80.179", "443"))

    def test_check_cloudflare_proxy(self):
        proxy = checker.IPChecker.check_cloudflare_proxy("104.19.32.25", "8443", True)
        print(proxy)
        proxy2 = checker.IPChecker.check_cloudflare_proxy("61.222.202.104", "23555", True)
        print(proxy2)


    def test_range(self):
        i = 2
        for a in range(i):
            print(a)

    def test_key_out(self):
        a = {"a":"b"}
        print(a["f"])
