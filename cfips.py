from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests

import config


@dataclass
class CFIPData:
    ip: str
    port: int
    is_secure: bool
    city_code: str
    region: str
    country: str
    latency: str
    download_speed: str


class CloudflareIPProvider(ABC):
    @abstractmethod
    def get_ips(self) -> [CFIPData]:
        pass


class AAAGroupIPProvider(CloudflareIPProvider):
    def get_ips(self) -> [CFIPData]:
        response = requests.get(config.GlobalConfig.cf_betterip_api)
        json_data = response.json()
        print()


if __name__ == '__main__':
    ip_provider = AAAGroupIPProvider()
    ips = ip_provider.get_ips()
    print(ips)
