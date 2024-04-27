import checker

if __name__ == '__main__':
    print(f"Welcome to auto-refresh-paimon cloud!")
    proxy = checker.IPChecker.check_cloudflare_proxy("104.19.32.25", "443", True)
    print(proxy)
