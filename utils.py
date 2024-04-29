import random
import time


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

def random_sleep(max_sleep: int = 1):
    sleep_time = random.uniform(0, max_sleep)
    # 生成一个介于 0 和 1 之间的随机小数
    time.sleep(sleep_time)


if __name__ == '__main__':
    db_url = "root:aabbcc@abc.mysql@apple.com:24306/apple"

    print(process_atin_dburl(db_url))
