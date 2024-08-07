import os

import redis

redis_host = os.getenv("REDIS_HOST", "127.0.0.1")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_pass = os.getenv("REDIS_PASS", "mypass")

pool = redis.ConnectionPool(
    host=redis_host,
    port=redis_port,
    db=1, password=redis_pass,
    socket_connect_timeout=60 * 60 * 6,
    socket_timeout=60 * 60 * 6,
    max_connections=4
)
# 适配的redis版本
# 初始化 Redis 连接
r = redis.Redis(connection_pool=pool,
                ssl=False)



