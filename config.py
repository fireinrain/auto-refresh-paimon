import os


class Config(object):
    def __init__(self):
        db_url = os.getenv("V2BoardDBUrl", "v2boardx.db")
        self.db_connect_url = db_url
        cf_betterip_api = os.getenv("CFBetterIPApi", "https://yx.xmsl.io/vmess/all")
        self.cf_betterip_api = cf_betterip_api


GlobalConfig = Config()
