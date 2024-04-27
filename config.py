import os


class Config(object):
    def __init__(self):
        # db_url 格式user:password@localhost/mydatabase
        db_url = os.getenv("V2BoardDBUrl", "v2boardx.db")
        self.db_connect_url = db_url
        cf_betterip_api = os.getenv("CFBetterIPApi", "https://yx.xmsl.io/vmess/all")
        self.cf_betterip_api = cf_betterip_api

        self.node_country_map = {
            '续订': ['SJC', 'US', 'LAX'],
            '不可用': ['SJC', 'US', 'LAX'],
            '香港': ['HKG', 'HK'],
            '澳门': ['MFM', 'MO'],
            '新加坡': ['SIN', 'SG'],
            '台湾': ['TPE', 'TW', 'KHH'],
            '日本': ['JP', 'NRT', 'KIX', 'OKA', 'FUK'],
            '韩国': ['KR', 'ICN'],
            '美国': ['SJC', 'US', 'LAX'],
            '英国': ['GB', 'EDI', 'LHR', 'MAN'],
            '法国': ['FR', 'CDG', 'MRS', 'LYS', 'BOD'],
            '德国': ['DE', 'TXL', 'DUS', 'FRA', 'HAM', 'STR', 'MUC'],
            '地球': ['TW', 'TPE', 'KHH']
        }

    def get_node_country_map(self):
        return self.node_country_map


GlobalConfig = Config()
