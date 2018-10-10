from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.response import BaseResponse
from api.utils.authentications import Authentication
from api.models import Course
from django.core.exceptions import ObjectDoesNotExist
from api.utils.myExceptions import CourseDoesNotExist,PriceDoesNotExist
from django.conf import settings
from django_redis import get_redis_connection
import json


class ShoppingCartView(ViewSetMixin,APIView):
    # 连接Redis服务器
    conn = get_redis_connection("default")

    # 一、用户认证 ==》 认证组件
    authentication_classes = [Authentication,]

    # 三、查看购物车 ==》 视图类的查看函数
    def list(self,request, *args, **kwargs):
        '''
        需求：用户点击购物车，即显示购物车中所有商品信息。
        方案：前端带着当前访问用户的token值向后端发送GET请求；
              后端根据redis的指令keys匹配到该用户购物车中所有课程的信息，并将其数据返回给前端。
        code: 1005 --> 获取购物车数据失败
        '''
        # 1. 获取响应数据的实例化对象
        response = BaseResponse()
        try:
            # 2. 获取当前访问用户的ID
            user_id = request.user.pk
            # 3. 自定义一个数据结构，存放购物车中的所有商品信息
            shopping_car_course_list = []
            '''
            redis:{
                "shopping_car_course_list":[
                    { 'course_id': 4,  'course_name': '网络编程入门&FTP服务开发实战', 'course_img':'/static/imgs/网络编程入门&FTP服务开发实战_1509095352.918334.png', 'default_price_id':10,  'price_policy_dict':{……}, },
                    { 'course_id': 2,  'course_name': 'Python开发21天入门', 'course_img':'/static/imgs/Python21天入门必备_1509095274.4902391.png', 'default_price_id':6,  'price_policy_dict':{……}, },
                ]
            }
           '''
            # 4. 获取Redis中当前访问用户的购物车的商品信息
            pattern = settings.SHOPPING_CAR_KEY.format(user_id,"*") # shopping_car_1_*
            user_keys_list = self.conn.keys(pattern) # [b'shopping_car_1_4', b'shopping_car_1_2']
            for user_keys in user_keys_list:
                temp = {
                    "course_id":int(user_keys.decode('utf-8').rsplit('_',1)[-1]),
                    "course_name":self.conn.hget(user_keys,"name").decode('utf-8'),
                    "course_img":self.conn.hget(user_keys,"course_img").decode('utf-8'),
                    "default_price_id":self.conn.hget(user_keys,"default_price_policy_id").decode('utf-8'),
                    "price_policy_dict":json.loads(self.conn.hget(user_keys,"relate_price_policy").decode('utf-8'))
                }
                shopping_car_course_list.append(temp)
            response.data = json.dumps(shopping_car_course_list)
        except Exception as e:
            response.code = 1005
            response.error = '获取购物车数据失败!'

        return Response(response.dict)

    # 二、添加购物车 ==》 视图类的增加函数
    def create(self,request, *args, **kwargs):
        '''
        需求：用户通过在浏览器上点选商品，将商品添加到购物车。
        方案：前端携带该访问用户token值，将商品ID 和 该商品所对应的价格策略ID 通过POST请求发送到后端；
              后端获取到商品ID 和 该商品所对应的价格策略ID，校验数据成功之后将数据存入Redis数据库中。
        code: 1000 --> 响应成功 ; 1001 --> 认证失败 ; 1002 --> 商品不存在 ; 1003 --> 价格策略不存在 ; 1004 --> 其他异常错误
        '''
        # 1、导入返回响应数据的基类，实例化得到响应数据对象
        response = BaseResponse()
        try:
            # 2、获取当前访问的用户ID
            user_id = request.user.pk   # request.user ==》认证组件中返回的userToken_obj.user
            # 3、获取前端发送过来的商品ID 和 相对应的价格策略ID
            course_id = request.data.get('course_id')
            price_policy_id = request.data.get('price_policy_id')
            # 4、对发送过来的数据进行校验
                # 4.1 校验用户所选的商品是否存在
            course_obj = Course.objects.get(pk=course_id)   # 获取不到对象就会报错，方便异常ObjectDoesNotExist捕获
                # 4.2 商品存在后，再校验 < 该商品所对应的价格策略 > 是否合法：
                    # 4.2.1 获取到该商品所对应的所有价格策略列表
            related_price_policy_list = course_obj.price_policy.all()
                    # 4.2.2 自定义一个字典，存放该商品所对应的所有价格策略信息，方便后期使用:
                        # price_policy_dict ==》{ 1: { "price":99,"valid_period":1,"valid_period_text":"1个月" }，2: { "price":88,"valid_period":3,"valid_period_text":"6个月" } }
            price_policy_dict = {}
            for price_policy_obj in related_price_policy_list:
                price_policy_dict[price_policy_obj.pk] = {
                    "price":price_policy_obj.price,
                    "valid_period":price_policy_obj.valid_period,
                    "valid_period_text":price_policy_obj.get_valid_period_display(),
                }
                    # 4.2.3 判断用户所选的价格策略ID是否在自定义的这个字典中，若不存在就抛出自定义的异常
            if price_policy_id not in price_policy_dict:
                raise PriceDoesNotExist
            # 5、商品和价格策略都校验成功后，将商品添加到购物车，存储到Redis数据库中
            '''
            方案1：
            user_id:{ shopping_car:{ course_id:{ name:"",img:"",price_policy:{},default_price_policy_id:3 }}}
            
            && redis接口1 &&  ==》 这样写是可以，但是每写一个接口都要写以下代码，过于麻烦
            import redis
            pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
            redis = redis.Redis(connection_pool=pool)
            
            方案2（推荐）：
            redis:{ shopping_car_1_2:{ name:"", img:"", price_policy:{}, default_price_policy_id:3 },
                    shopping_car_1_3:{ name:"", img:"", price_policy:{}, default_price_policy_id:3 },
                    shopping_car_2_1:{ name:"", img:"", price_policy:{}, default_price_policy_id:3 },
                   }
            && redis接口2 &&  ==》 这样写就在配置类中配置一下，以后每写一个接口只要写以下代码即可
            django-redis模块
            redis=get_redis_connection("default")    
            '''
            # conn = get_redis_connection("default")
            shopping_car_key = settings.SHOPPING_CAR_KEY.format(user_id,course_id)
            course_info = {
                "name":course_obj.name,
                "course_img":course_obj.course_img,
                "relate_price_policy":json.dumps(price_policy_dict),
                "default_price_policy_id":price_policy_id
            }
            self.conn.hmset(shopping_car_key,course_info)
            response.data = '加入购物车成功！'

        except ObjectDoesNotExist as e:
            response.code = 1002
            response.error = '您所选的商品不存在！'

        except PriceDoesNotExist as e:
            response.code = 1003
            response.error = e.error

        except Exception as e:
            response.code = 1004
            response.error = str(e)

        return Response(response.dict)

    # 五、编辑购物车 ==》 视图类的编辑函数
    def update(self,request, *args, **kwargs):
        '''
        需求：用户在浏览器上点选商品有效期，即修改了购物车中该商品的价格策略。
        方案：前端 携带着要编辑的商品ID 通过POST请求 将修改的默认价格策略ID 发送到后端；
              后端获取到商品ID 和 新的价格策略ID ，对获取到的数据进行校验成功后，将新的价格策略修改到数据库Redis中。
        code: 1008 --> 该商品修改失败
        '''
        # 1. 获取响应实例化对象
        response = BaseResponse()
        # 2. 获取当前访问用户ID
        user_id = request.user.pk
        # 3. 获取要编辑的商品ID
        course_id = kwargs.get('pk')    # '2'
        # 4. 获取新的默认价格策略ID
        new_default_price_policy_id = str(request.data.get('default_price_policy_id'))
        # 5. 对获取到的数据进行校验
        try:
            # 5.1 首先校验获取的商品ID 是否在购物车中的商品,若没有此键则抛出异常
            shopping_car_key = settings.SHOPPING_CAR_KEY.format(user_id,course_id)
            if not self.conn.exists(shopping_car_key):
                raise CourseDoesNotExist
            # 5.2 商品ID校验成功后，校验获取的新的默认价格策略ID是否在在购物车该商品的所有的有效价格策略中
            all_valid_price_policy_dict = json.loads(self.conn.hget(shopping_car_key,'relate_price_policy').decode('utf-8'))
            if new_default_price_policy_id not in all_valid_price_policy_dict:
                raise PriceDoesNotExist
            # 6.将新的价格策略修改到数据库Redis中
            self.conn.hset(shopping_car_key,'default_price_policy_id',new_default_price_policy_id)
            # 7.给购物车中该商品设置超时时间，超出设定时间就会该商品信息就会失效、
            self.conn.expire(shopping_car_key,20 * 60)
            response.data = '该商品修改成功！'

        except CourseDoesNotExist as e:
            response.code = 1006
            response.error = e.error

        except PriceDoesNotExist as e:
            response.code = 1003
            response.error = e.error

        except Exception as e:
            response.code = 1008
            response.error = '该商品修改失败！'

        return Response(response.dict)

    # 四、删除购物车 ==》 视图类的删除函数
    def destroy(self,request,*args,**kwargs):
        '''
        需求：用户选中购物车中的某个商品，点击删除，即删除购物车中此商品信息。
        方案：前端将携带着 删除的商品ID 发送到后端；
              后端获取到商品ID 和 用户ID 后，通过删除Redis中的键来删除购物车中该商品信息。
        code : 1006 --> 用户所选的商品不在购物车中 ; 1007 --> 购物车中的该商品删除失败
        '''
        # 1. 获取响应数据的实例化对象
        response = BaseResponse()
        try:
            # 2. 获取当前访问用户ID
            user_id = request.user.pk
            # 3. 获取前端发送过来的商品ID
            course_id = kwargs.get('pk')
            # 4. 通过获取到的用户ID 和 商品ID 来获取Redis中的键
            shopping_car_key = settings.SHOPPING_CAR_KEY.format(user_id,course_id)
            # 5. 校验购物车中是否有此键，若没有此键则抛出异常
            if not self.conn.exists(shopping_car_key):
                raise CourseDoesNotExist
            # 6. 校验成功后，通过键删除购物车中的此商品信息
            self.conn.delete(shopping_car_key)
            # 7. 删除成功后，返回给前端消息
            response.data = '购物车中的该商品已删除！'
        except CourseDoesNotExist as e:
            response.code = 1006
            response.error = e.error
        except Exception as e:
            response.code = 1007
            response.error = '购物车中的该商品删除失败！'
        return Response(response.dict)
