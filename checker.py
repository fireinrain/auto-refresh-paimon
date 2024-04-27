import http.client
import random
import re
import socket
import ssl
import time
from urllib.parse import urlparse

import requests

import locations


class IPChecker:
    @staticmethod
    def check_port_open(host: socket, port: str | int, retry: int = 1, threshold: int = 1) -> bool:
        sock = None
        port = int(port)
        success_count = 0
        for i in range(retry):
            try:
                # Create a socket object
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Set timeout to 1 second
                sock.settimeout(2.)
                # Connect to the host and port
                result = sock.connect_ex((host, port))
                if result == 0:
                    print(f">>> Port {port} is open on {host}")
                    success_count += 1
                else:
                    print(f">>> Port {port} is closed on {host}")

            except Exception as e:
                print(f"Error checking port: {e}")
            finally:
                sock.close()
        if success_count >= threshold and success_count > 0:
            return True
        return False

    # 检测ip端口是否被gfw ban
    @staticmethod
    def check_baned_with_gfw(host: str, port: str | int) -> bool:
        request_url = f"https://www.toolsdaquan.com/toolapi/public/ipchecking/{host}/{port}"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,ja;q=0.6",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "https://www.toolsdaquan.com/ipcheck/",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"macOS\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest"
        }
        random_user_agent = IPChecker.get_random_user_agent()
        headers['User-Agent'] = random_user_agent

        try:
            resp = requests.get(request_url, headers=headers)
            resp.raise_for_status()

            response_data = resp.json()

            if response_data['icmp'] == "success" and response_data['tcp'] == "success":
                print(f">>> ip: {host}:{port} is ok in China!")
                return False
            else:
                print(f">>> ip: {host}:{port} is banned in China!")
                return True
        except Exception as e:
            print(">>> Error request for ban check:", e)
            return True

    @staticmethod
    def get_random_user_agent() -> str:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
        ]

        return random.choice(user_agents)

    @staticmethod
    def check_cloudflare_proxy(host: str, port: str | int, tls: bool = True) -> [bool, {}]:

        ip = host
        port = int(port)
        test_url = 'speed.cloudflare.com/cdn-cgi/trace'
        if tls:
            url = f'https://{test_url}'
        else:
            url = f'http://{test_url}'
        parsed_url = urlparse(url)
        path = parsed_url.path
        if not path:
            path = '/'

        start_time = time.time()

        connection = None
        if parsed_url.scheme == 'http':
            connection = http.client.HTTPConnection(ip, port)
        elif parsed_url.scheme == 'https':
            context = ssl.create_default_context()
            connection = http.client.HTTPSConnection(ip, port, context=context)
        else:
            print(f">>> Unsupported URL scheme")
            return [False, {}]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
        }
        try:
            connection.request("GET", path, headers=headers)
            response = connection.getresponse()
            # Calculate the total time taken for both operations
            total_duration = f'{(time.time() - start_time) * 1000:.2f}'
            print(f'Total tcp connection duration: {total_duration} ms')
            resp = response.read().decode()
            location = IPChecker.detect_cloudflare_location(host, port, resp, str(total_duration))
            if location is None:
                return [False, {}]
            return [True, location]
        except Exception as e:
            print(f">>> Connection failed of: {e}")
            return [False, {}]
        finally:
            if connection:
                connection.close()

    @staticmethod
    def detect_cloudflare_location(ip_addr: str, port: int | str, body: str, tcpDuration: str) -> dict | None:
        if 'uag=Mozilla/5.0' in body:
            matches = re.findall('colo=([A-Z]+)', body)
            if matches:
                dataCenter = matches[0]  # Get the first match
                loc = locations.CloudflareLocationMap.get(dataCenter)
                if loc:
                    print(f"发现有效IP {ip_addr} 端口 {port} 位置信息 {loc['city']} 延迟 {tcpDuration} 毫秒")
                    # Append a dictionary to resultChan to simulate adding to a channel
                    return {
                        "ipAddr": ip_addr,
                        "port": port,
                        "dataCenter": dataCenter,
                        "region": loc['region'],
                        "city": loc['city'],
                        "latency": f"{tcpDuration} ms",
                        "tcpDuration": tcpDuration
                    }
                print(f"发现有效IP {ip_addr} 端口 {port} 位置信息未知 延迟 {tcpDuration} 毫秒")
                # Append a dictionary with some empty fields to resultChan
                return {
                    "ipAddr": ip_addr,
                    "port": port,
                    "dataCenter": dataCenter,
                    "region": "",
                    "city": "",
                    "latency": f"{tcpDuration} ms",
                    "tcpDuration": tcpDuration
                }

        return None
