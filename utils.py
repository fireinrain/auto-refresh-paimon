def process_atin_dburl(dburl: str) -> str:
    dburl_split = dburl.split("@")
    if len(dburl_split) == 3:
        from urllib.parse import quote
        db_link = dburl_split[0] + quote("@") + dburl_split[1] + "@" + dburl_split[2]
        return db_link

    return dburl


if __name__ == '__main__':
    db_url = "root:aabbcc@abc.mysql@apple.com:24306/apple"

    print(process_atin_dburl(db_url))
