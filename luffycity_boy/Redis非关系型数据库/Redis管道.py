'''
redis-py默认在执行每次请求都会创建（连接池申请连接）和断开（归还连接池）一次连接操作，如果想要在一次请求中指定多个命令，则可以使用pipline实现一次请求指定多个命令，并且默认情况下一次pipline 是原子性操作。
'''
import redis
# 连接 连接池
pool = redis.ConnectionPool(host='127.0.0.1',port=6379)
r = redis.Redis(connection_pool=pool)

# 设置管道
pipe = r.pipeline(transaction=True)
# 事务开始
pipe.multi()


##### 原事务 开始  #####
# pipe.set('name','alex')
# pipe.set('age',27)
# print(r.get('name'))    # b'alex'
# print(r.get('age'))     # b'27'
##### 原事务 结束  #####

##### 新事务 开始  #####
pipe.set('name','egon')
pipe.set('user_info',{'name':'yangqian'})   # 出现错误的指令，回滚到原事务
pipe.set('age',25)
print(r.get('name'))    # b'alex'
print(r.get('age'))     # b'27'
##### 新事务 结束  #####

# 执行，把所有命令一次性推送过去
pipe.execute()


