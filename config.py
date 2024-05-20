import os


class Config(object):
    def __init__(self):
        # db_url 格式user:password@localhost/mydatabase
        db_url = os.getenv("V2BOARDDBURL", "v2boardx.db")
        print(f">>> Current database url: {db_url}")
        self.db_connect_url = db_url
        cf_betterip_api = os.getenv("CFBetterIPApi", "https://yx.xmsl.io/vmess/all")
        self.cf_betterip_api = cf_betterip_api
        self.shared_cf_sublinks = os.getenv("SHAREDCFSUBLINKS", "")

        self.node_country_map = {
            '续订': ['US', 'SJC', 'LAX'],
            '不可用': ['US', 'SJC', 'LAX'],
            '香港': ['HK', 'HKG'],
            '澳门': ['MO', 'MFM'],
            '新加坡': ['SG', 'SIN'],
            '台湾': ['TW', 'TPE', 'KHH'],
            '日本': ['JP', 'NRT', 'KIX', 'OKA', 'FUK'],
            '韩国': ['KR', 'ICN'],
            '美国': ['US', 'SJC', 'LAX'],
            '英国': ['GB', 'EDI', 'LHR', 'MAN'],
            '法国': ['FR', 'CDG', 'MRS', 'LYS', 'BOD'],
            '德国': ['DE', 'TXL', 'DUS', 'FRA', 'HAM', 'STR', 'MUC'],
            '地球': ['TW', 'TPE', 'KHH'],
            '太阳': ['US', 'SJC', 'LAX']
        }

    def get_node_country_map(self):
        return self.node_country_map


GlobalConfig = Config()
