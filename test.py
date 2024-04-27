from unittest import TestCase

import checker


class TestIPChecker(TestCase):
    def test_check_port_open(self):
        print(checker.IPChecker.check_port_open("127.0.0.1", "22"))

    def test_check_baned_with_gfw(self):
        print(checker.IPChecker.check_baned_with_gfw("220.130.80.179", "443"))

    def test_check_cloudflare_proxy(self):
        proxy = checker.IPChecker.check_cloudflare_proxy("104.19.32.25", "443", True)
        print(proxy)
