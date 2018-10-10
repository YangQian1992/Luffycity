import redis
r = redis.Redis(host='127.0.0.1',port=6379)


'''
# 连接redis服务器的第一种方式 #
r = redis.Redis(host='127.0.0.1',port=6379)
r.set('name','杨倩')
print(r.get('name').decode('utf-8'))    # 杨倩

# 连接redis服务器的第二种方式 #
pool = redis.ConnectionPool(host='127.0.0.1',port=6379)
r = redis.Redis(connection_pool=pool)
r.set('name','张贝贝')
print(r.get('name').decode('utf-8'))    # 张贝贝
'''


'''
$ 字符串操作：Redis中的字符串在内存中按照一个键对应一个值来存储 $
r.set('age',27)
print(r.get('age')) # b'27'

r.setnx('name','alex')
print(r.get('name').decode('utf-8'))    # 张贝贝

r.mset(name='yangqian',age='27')
print(r.mget('name','age')) # [b'yangqian', b'27']

r.mset({'name':'yangqian','age':'27'})
print(r.mget(['name','age']))   #[b'yangqian', b'27']

# getset(name,value):设置新值并获取原来的值
r.set('name','alex')
print(r.getset('name','egon'))  # b'alex'
print(r.get('name'))    # b'egon'

# getrange(key,start,end):对键所对应的值进行切片（顾头也顾尾）
r.set('name','alex')
print(r.getrange('name',1,3))   # b'lex'

# setrange(name, offset, value):修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加）
r.set('msg','杨倩是个学霸')
r.setrange('msg',0,'张贝贝')
print(r.get('msg').decode('utf-8')) # 张贝贝个学霸

# strlen(name):返回name对应值的字节长度（一个汉字3个字节）
r.set('name','alex')
print(r.strlen('name')) # 4
r.set('name','中国')
print(r.strlen('name')) # 6

# incr(self, name, amount=1):自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
r.set('age','27')
r.incr('age',2)
print(r.get('age')) # b'29'

r.set('age','27')
r.incrbyfloat('age',2.5)
print(r.get('age')) # b'29.5'

r.set('age','27')
r.decr('age',7)
print(r.get('age')) # b'20'

# append(key,value):拼接字符串（在后面追加）
r.set('msg','杨倩')
r.append('msg','hello!')
print(r.get('msg').decode('utf-8')) # 杨倩hello!
'''


'''
$ Hash操作 $
r.hset('shopping_cart','price',22)
print(r.hget('shopping_cart','price'))  # b'22'

r.hmset('shopping_cart',{'course_id':1,'course_name':'Python','price':22,})
print(r.hmget('shopping_cart','course_id'))   # [b'1']
print(r.hmget('shopping_cart','course_id','course_name'))   # [b'1', b'Python']
print(r.hgetall('shopping_cart'))   # {b'price': b'22', b'course_id': b'1', b'course_name': b'Python'}

print(r.hlen('shopping_cart'))  # 3

print(r.hkeys('shopping_cart')) # [b'price', b'course_id', b'course_name']
print(r.hvals('shopping_cart')) # [b'22', b'1', b'Python']

print(r.hexists('shopping_cart','course'))  # False
print(r.hexists('shopping_cart','course_name'))  # True
print(r.exists('shopping_cart'))    # True

print(r.hdel('shopping_cart','course')) # 0
print(r.hdel('shopping_cart','course_id')) # 1
print(r.hgetall('shopping_cart')) # {b'price': b'22', b'course_name': b'Python'}

print(r.hincrby('shopping_cart',2)) # 1
print(r.hgetall('shopping_cart'))   # {b'price': b'22', b'course_name': b'Python', b'2': b'1'}

print(r.hincrby('shopping_cart','price',2))   # 24
print(r.hincrbyfloat('shopping_cart','2',88.88))    # 89.88

# hash操作中的踩坑点:hmset(name, mapping)==》 批量添加时，是看最外层的键所对应的值中的键值对是否存在。如果添加的redis最外层的键已存在，原键所对应的值中没有的就添加，有的就覆盖
r.hmset('user_info',{'name':'yangqian','age':27,'hobbies':['烫头','美甲']})
print(r.hgetall('user_info'))   # {b'name': b'yangqian', b'age': b'27', b'hobbies': b"['\xe7\x83\xab\xe5\xa4\xb4', '\xe7\xbe\x8e\xe7\x94\xb2']"}
r.hmset('user_info',{'job':'IT','salary':10000,'age':25})
print(r.hgetall('user_info'))   # {b'name': b'yangqian', b'age': b'25', b'hobbies': b"['\xe7\x83\xab\xe5\xa4\xb4', '\xe7\xbe\x8e\xe7\x94\xb2']", b'job': b'IT', b'salary': b'10000'}

# hscan_iter(name, match=None, count=None):利用yield封装hscan创建生成器，实现分批去redis中获取数据
for item in r.hscan_iter('user_info'):
    print(item)
    # (b'name', b'yangqian')
    # (b'age', b'25')
    # (b'hobbies', b"['\xe7\x83\xab\xe5\xa4\xb4', '\xe7\xbe\x8e\xe7\x94\xb2']")
    # (b'job', b'IT')
    # (b'salary', b'10000')

# hscan(name, cursor=0, match=None, count=None):增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，并非一次性将数据全部获取完，从而放置内存被撑爆(前提是：有成千上万条数据才会分片)
print(r.hscan('user_info',2))   # (0, {b'name': b'yangqian', b'age': b'25', b'hobbies': b"['\xe7\x83\xab\xe5\xa4\xb4', '\xe7\xbe\x8e\xe7\x94\xb2']", b'job': b'IT', b'salary': b'10000'})
'''


'''
$ List操作 $
r.lpush('students','alex','taibai','egon')
print(r.llen('students'))   # 3
print(r.lrange('students',0,1)) # [b'egon', b'taibai']
print(r.lrange('students',0,r.llen('students')-1)) # [b'egon', b'taibai', b'alex']

# lpushx(name,value):在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边
r.lpushx('students','yangqian')
print(r.lrange('students',0,r.llen('students')-1))  # [b'yangqian', b'egon', b'taibai', b'alex']

# rpushx(name, value):在name对应的list中添加元素，只有name已经存在时，值添加到列表的最右边
r.rpush('students','zhangbeibei')
print(r.lrange('students',0,r.llen('students')))    # [b'yangqian', b'egon', b'taibai', b'alex', b'zhangbeibei']

r.linsert('students','BEFORE','alex','wanrong')
print(r.lrange('students',0,r.llen('students')))    # [b'yangqian', b'egon', b'taibai', b'wanrong', b'alex', b'zhangbeibei']

r.linsert('students','AFTER','egon','yuanhao')
print(r.lrange('students',0,r.llen('students'))) # [b'yangqian', b'egon', b'yuanhao', b'taibai', b'wanrong', b'alex', b'zhangbeibei']

# r.lset(name, index, value)：对name对应的list中的某一个索引位置重新赋值
r.lset('students',3,'nezha')
print(r.lrange('students',0,r.llen('students')))    # [b'yangqian', b'egon', b'yuanhao', b'nezha', b'wanrong', b'alex', b'zhangbeibei']

# r.lrem(name, value, num):在name对应的list中删除指定的值
r.lset('students',6,'nezha')
print(r.lrange('students',0,r.llen('students')))    # [b'yangqian', b'egon', b'yuanhao', b'nezha', b'wanrong', b'alex', b'nezha']
r.lrem('students','nezha',1)
print(r.lrange('students',0,r.llen('students')))    # [b'yangqian', b'egon', b'yuanhao', b'wanrong', b'alex', b'nezha']
r.lset('students',0,'nezha')
print(r.lrange('students',0,r.llen('students')))    # [b'nezha', b'egon', b'yuanhao', b'wanrong', b'alex', b'nezha']
r.lrem('students','nezha',-1)
print(r.lrange('students',0,r.llen('students')))    # [b'nezha', b'egon', b'yuanhao', b'wanrong', b'alex']
r.lset('students',1,'nezha')
print(r.lrange('students',0,r.llen('students')))    # [b'nezha', b'nezha', b'yuanhao', b'wanrong', b'alex']
r.lrem('students','nezha')
print(r.lrange('students',0,r.llen('students')))    # [b'yuanhao', b'wanrong', b'alex']


# lpop(name):在name对应的列表的左侧获取第一个元素并在列表中移除，返回值则是第一个元素
print(r.lrange('students',0,r.llen('students')))    # [b'yuanhao', b'wanrong', b'alex']
print(r.lpop('students'))  # b'yuanhao'
print(r.lrange('students',0,r.llen('students'))) # [b'wanrong', b'alex']

print(r.lrange('students',0,r.llen('students')))    # [b'wanrong', b'alex']
print(r.rpop('students'))   # b'alex'
print(r.lrange('students',0,r.llen('students')))    # [b'wanrong']

r.lpush('students','alex','taibai','nezha','yuanhao','wusir')
print(r.lrange('students',0,r.llen('students')))    # [b'wusir', b'yuanhao', b'nezha', b'taibai', b'alex', b'wanrong']
print(r.lindex('students',3))   # b'taibai'

# ltrim(name, start, end):在name对应的列表中移除没有在start-end索引之间的值
print(r.lrange('students',0,r.llen('students')-1))  # [b'wusir', b'yuanhao', b'nezha', b'taibai', b'alex', b'wanrong']
print(r.ltrim('students',2,4))  # True
print(r.lrange('students',0,r.llen('students')-1))  # [b'nezha', b'taibai', b'alex']

print(r.lrange('students',0,r.llen('students')-1))  # [b'nezha', b'taibai', b'alex']
print(r.ltrim('students',2,4))  # True
print(r.lrange('students',0,r.llen('students')-1))  # [b'alex']

print(r.lrange('students',0,r.llen('students')-1))  # [b'alex']
print(r.ltrim('students',2,4))  # True
print(r.lrange('students',0,r.llen('students')-1))  # []
'''


'''
print(r.delete('students')) # 0
print(r.exists('students')) # False

print(r.delete('user_info')) # 1
print(r.exists('user_info')) # False

# Keys 命令用于查找所有符合给定模式 pattern 的 key 。
print(r.keys('shopping_car*'))  # [b'shopping_cart', b'shopping_car_1_2']
# delete 可以模糊删除
print(r.keys('*e'))     # [b'age',b'name']
ret = r.keys('*e')
print(r.delete(*ret))   # 2
print(r.keys('*e'))    # []
'''

# print(r.keys())
# [b'shopping_car_1_4', b'global_coupon_1', b'course_account_1_4']



