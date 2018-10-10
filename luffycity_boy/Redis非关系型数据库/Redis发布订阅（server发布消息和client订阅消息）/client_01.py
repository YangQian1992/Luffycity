import redis

conn = redis.Redis()

# Redis client 订阅消息
pub = conn.pubsub()
pub.subscribe('fm104.5')
pub.parse_response()

while True:
    print('working……')
    msg = pub.parse_response()
    print(msg)

    '''
    working……
    [b'message', b'fm104.5', b'hello world!!!']
    working……
    '''