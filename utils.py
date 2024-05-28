import random
import time
import socket


def process_atin_dburl(dburl: str) -> str:
    dburl_split = dburl.split("@")
    if len(dburl_split) == 3:
        from urllib.parse import quote
        db_link = dburl_split[0] + quote("@") + dburl_split[1] + "@" + dburl_split[2]
        return db_link

    return dburl


def detect_country_by_keyword(country_map: dict, keyword: str) -> [str]:
    keys = country_map.keys()
    try:
        for k in keys:
            if k in keyword:
                data = country_map[k]
                return data
    except KeyError:
        # 默认设置为US
        print(f">>> country_map key error: {keyword},use US as default")

    return ['US', 'SJC', 'LAX']


SPECIAL_CHARS = [
    '\\',
    '_',
    '*',
    '[',
    ']',
    '(',
    ')',
    '~',
    '`',
    '>',
    '<',
    '&',
    '#',
    '+',
    '-',
    '=',
    '|',
    '{',
    '}',
    '.',
    '!'
]


def clean_str_for_tg(data_str: str) -> str:
    for char in SPECIAL_CHARS:
        data_str = data_str.replace(char, f'\\{char}')
    return data_str


def random_sleep(max_sleep: int = 1):
    sleep_time = random.uniform(0, max_sleep)
    # 生成一个介于 0 和 1 之间的随机小数
    time.sleep(sleep_time)


def get_ip_address(domain: str) -> str:
    try:
        # 获取IPv4地址
        ipv4 = socket.gethostbyname(domain)
        print(f"IPv4 address of {domain}: {ipv4}")
        return ipv4
    except socket.gaierror:
        print(f"Could not resolve {domain} to an IPv4 address")

    try:
        # 获取IPv6地址
        ipv6_info = socket.getaddrinfo(domain, None, socket.AF_INET6)
        ipv6_addresses = [info[4][0] for info in ipv6_info]
        # 去重
        ipv6_addresses = list(set(ipv6_addresses))
        for ipv6 in ipv6_addresses:
            print(f"IPv6 address of {domain}: {ipv6}")
        return ipv6_addresses[0]
    except socket.gaierror:
        print(f"Could not resolve {domain} to an IPv6 address")
    return ""


import re
import socket


def is_valid_ipv4(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if pattern.match(ip):
        # Further check to ensure each segment is between 0 and 255
        segments = ip.split('.')
        if all(0 <= int(segment) <= 255 for segment in segments):
            return True
    return False


def is_valid_ipv6(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except socket.error:
        return False


def is_valid_hostname(hostname):
    # Valid hostname regex based on RFC 1034 and RFC 1123
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    # Hostnames must not be all numeric and must follow the rules
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def identify_string(s):
    if is_valid_ipv4(s):
        return "IPv4"
    elif is_valid_ipv6(s):
        return "IPv6"
    elif is_valid_hostname(s):
        return "Hostname"
    else:
        return "Invalid"


# 示例域名
domain = "www.example.com"
get_ip_address(domain)

if __name__ == '__main__':
    db_url = "root:aabbcc@abc.mysql@apple.com:24306/apple"

    print(process_atin_dburl(db_url))
