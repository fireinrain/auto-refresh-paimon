import csv
import json
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests
import yaml
import config
import utils
from redistools import r


@dataclass
class CFIPData:
    ip: str = ""
    port: int = 0
    tls: bool = True
    city_code: str = ""
    region: str = ""
    country: str = ""
    latency: str = ""
    download_speed: str = ""


class CloudflareIPProvider(ABC):
    @abstractmethod
    def get_ips(self) -> [CFIPData]:
        pass


class AAAGroupIPProvider(CloudflareIPProvider):
    def get_ips(self) -> [CFIPData]:
        try:
            response = requests.get(config.GlobalConfig.cf_betterip_api)
            response.raise_for_status()
            json_data = response.json()
            ip_datas = json_data['data']
            result = []
            for data in ip_datas:
                cfip_data = CFIPData()
                cfip_data.ip = data['host']
                cfip_data.port = data['port']
                cfip_data.country = data['country']
                result.append(cfip_data)
            return result
        except Exception as e:
            print(f">>> Get cloudflare ips from AAA failed: {e}")
            return []


class CSVFileIPProvider(CloudflareIPProvider):
    def get_ips(self) -> [CFIPData]:
        csv_files = self.read_csv_files("./cloudflare-ips")
        result = []
        for ip in csv_files:
            cfip_data = CFIPData()
            cfip_data.ip = ip['ip']
            cfip_data.port = 443
            cfip_data.country = ip['country']
            cfip_data.tls = True
            result.append(cfip_data)
        # print(csv_files)
        return result

    @staticmethod
    def read_csv_files(directory: str) -> [{}]:
        data_list = []

        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                        csv_reader = csv.reader(csvfile)
                        for row in csv_reader:
                            # Assuming each row has exactly 3 fields
                            if len(row) == 3:
                                data_list.append({'ip': row[0], 'ipv6': row[1], 'country': row[2]})

        return data_list


class SharedCFSublinksIPProvider(CloudflareIPProvider):
    def get_ips(self) -> [CFIPData]:
        sublinks = config.GlobalConfig.shared_cf_sublinks
        if not sublinks:
            return []

        sublinks_split = sublinks.split(",")
        headers = {
            "User-Agent": 'clash-meta'
        }
        result = []
        for link in sublinks_split:
            try:
                response = requests.get(link, headers=headers)
                response.raise_for_status()
                text = response.text
                if '@cf_no1' in text:
                    text = re.sub(r'[^\u0000-\u007F]+', '', text)
                yml_config = yaml.safe_load(text)
                proxies_ = yml_config['proxies']
                proxies_ = [p for p in proxies_ if p['type'] == 'vless']
                for proxy in proxies_:
                    node_name = proxy['name']
                    port = proxy['port']
                    server = proxy['server']
                    tls = proxy['tls']
                    cfip_data = CFIPData()
                    cfip_data.ip = server
                    cfip_data.port = port
                    cfip_data.tls = tls
                    node_name = utils.detect_cfno1_node_region_by_keyword(node_name)
                    country = utils.detect_country_by_keyword(config.GlobalConfig.get_node_country_map(), node_name)[0]
                    cfip_data.country = country

                    result.append(cfip_data)
            except Exception as e:
                print(f"Fetch ShareCFSublinks failed: {e}, line: {link}")
        return result


class IpdbBestCFIPProvider(CloudflareIPProvider):
    def get_ips(self) -> [CFIPData]:
        result = []
        url = "https://ipdb.api.030101.xyz/?type=bestproxy&country=true"
        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            resp_text = response.text
            text_split = resp_text.split("\n")
            for line in text_split:
                line_split = line.split("#")
                ip = line_split[0]
                port = 443
                loc = line_split[1]
                cfip_data = CFIPData()
                cfip_data.ip = ip
                cfip_data.port = port
                cfip_data.tls = True
                cfip_data.country = loc
                result.append(cfip_data)
        except Exception as e:
            print(f"Error on get url: {url},error: {e}")

        return result


class OpenPortSnifferRedisProvider(CloudflareIPProvider):
    def get_ips(self) -> [CFIPData]:
        result = []
        keys = r.hkeys('snifferx-result')

        # For each key, get the value and store in Cloudflare KV
        for key in keys:
            value = r.hget('snifferx-result', key)

            # Prepare the data for Cloudflare KV
            # kv_key = key.decode('utf-8')
            kv_value = json.loads(value.decode('utf-8'))

            cfip_data = CFIPData()
            cfip_data.ip = kv_value['ip']
            cfip_data.port = kv_value['port']
            cfip_data.tls = kv_value['enable_tls']
            datacenter = kv_value['data_center']
            country = utils.detect_country_by_dc_keyword(config.GlobalConfig.get_dc_country_map(), datacenter)
            cfip_data.country = country

            result.append(cfip_data)
        return result


if __name__ == '__main__':
    # ip_provider = AAAGroupIPProvider()
    # ips = ip_provider.get_ips()
    # print(ips)
    # ip_provider = CSVFileIPProvider()
    # ips = ip_provider.get_ips()
    # print(ips)
    # ip_provider = SharedCFSublinksIPProvider()
    # ip_provider.get_ips()

    # cfip_provider = IpdbBestCFIPProvider()
    # cfip_provider.get_ips()

    redis_provider = OpenPortSnifferRedisProvider()
    redis_provider.get_ips()
