import redis

conn = redis.Redis()

# Redis client 订阅消息
pub = conn.pubsub()
pub.subscribe('fm104.6')
pub.parse_response()

while True:
    print('working……')
    msg = pub.parse_response()
    print(msg)

    '''
    working……
    '''