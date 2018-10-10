import redis

conn = redis.Redis()

while True:
    msg = input('>>>')
    # Redis server 发布消息
    conn.publish('fm104.5',msg)