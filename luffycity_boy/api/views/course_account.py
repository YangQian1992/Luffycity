from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.response import BaseResponse
from api.utils.authentications import Authentication
from api.models import Course,CouponRecord
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django_redis import get_redis_connection
import json
import datetime


class CourseAccountView(ViewSetMixin,APIView):
    # 连接Redis服务器
    conn = get_redis_connection("default")

    # 一、用户认证 ==》 认证组件
    authentication_classes = [Authentication,]

    # 二、添加结算的商品 ==》 视图类的增加函数
    def create(self, request, *args, **kwargs):
        '''
        需求：用户通过在浏览器上点选商品（可多选），点击结算后，则成功添加结算的商品。
        方案：前端携带该访问用户token值，将所选的所有商品ID 通过POST请求发送到后端；
              后端获取到商品ID 和 该商品所对应的价格策略ID，校验数据成功之后将数据存入Redis数据库中。
        code: 1000 --> 响应成功 ; 1001 --> 认证失败 ; 1002 --> 商品不存在 ; 1003 --> 其他异常错误
        '''
        # 1、导入返回响应数据的基类，实例化得到响应数据对象
        response = BaseResponse()
        try:
            # 2、获取当前访问的用户ID
            user_id = request.user.pk  # request.user ==》认证组件中返回的userToken_obj.user
            # 3、获取当前访问用户结算中所有商品
            user_all_course_list_of_account = settings.COURSE_ACCOUNT_KEY.format(user_id,"*")
            course_account_keys_list = self.conn.keys(user_all_course_list_of_account)
            # 4、清除当前访问用户的结算中的数据
            if course_account_keys_list:
                self.conn.delete(*course_account_keys_list)
            # 5、获取前端发送过来的所有商品ID
            course_id_list = request.data.get('course_id')   # course_id--> [2, 4]
            # 6、设置Redis最外层键所对应的值是global_coupon_value(通用优惠券)
            global_coupon_value = {}
            # 7、对发送过来的数据进行校验
            for course_id in course_id_list:
                # 7.1 校验用户所选的商品是否存在,获取不到对象就会报错，方便异常ObjectDoesNotExist捕获
                course_obj = Course.objects.get(pk=course_id)
                # 7.2 商品校验成功后，设置结算接口的数据结构
                '''
                Redis:{
                    course_account_userID_courseID:{
                        course_detail:{
                            course_name:'',
                            course_img:'',
                            default_price_price_policy_id:'',
                            price_policy:{}
                        },
                        course_coupon:{
                            coupon_record_id:{
                                coupon_name:'',
                                coupon_type:'',
                                money_equivalent_value:'',
                                off_percent:'',
                                mininum_cousume:'',
                                object_id:''
                            }
                        }
                    },
                    global_coupon:{
                        coupon_record_id:{
                            coupon_name:'',
                            coupon_type:'',
                            money_equivalent_value:'',
                            off_percent:'',
                            mininum_cousume:'',
                            object_id:''
                        }                    
                    }
                }
              '''
                # 设置Redis最外层键所对应的值是course_account_value,这个值又拥有两个键值对，键分别是：course_detail 和 course_coupon
                course_account_value = {}
                course_detail_value = {}    # 键course_detail所对应的值
                course_coupon_vaule = {}    # 键course_coupon所对应的值
                # 7.3 从购物车中获取该商品信息
                shopping_cart_key = settings.SHOPPING_CAR_KEY.format(user_id,course_id)
                course_info = self.conn.hgetall(shopping_cart_key)
                # 7.4 循环处理课程信息,获取键course_detail所对应的值
                for key,value in course_info.items():
                    # 由于course_info字典中嵌套字节型字典，故解析出来嵌套的典是字符串型的字典。
                        # --> 解决方案：将字节解析成字符串后，再序列化。判断遍历的key值是否为“relate_price_policy”
                    if key.decode('utf-8') == "relate_price_policy":
                        course_detail_value[key.decode('utf-8')] = json.loads(value.decode('utf-8'))
                    else:
                        course_detail_value[key.decode('utf-8')] = value.decode('utf-8')
                # 7.5 将课程详细信息添加到course_account_value中
                course_account_value["course_detail"] = json.dumps(course_detail_value)
                # 7.6 获取< 用户> <所有的> <有效> <优惠券记录> ==》 有效：a.未使用 b.优惠券使用时间要大于有效期开始时间，小于有效期结束时间
                use_coupon_time = datetime.datetime.now()   # 优惠券使用时间
                user_all_coupon_record_queryset = CouponRecord.objects.filter(user=request.user,
                                                                     status=0,
                                                                     coupon__valid_begin_date__lt=use_coupon_time,
                                                                     coupon__valid_end_date__gt=use_coupon_time,
                                        )   # QuerySet对象集合
                # 7.7 遍历所有优惠券记录，获取每一个优惠券记录对象
                for coupon_record_obj in user_all_coupon_record_queryset:
                    coupon_info = {
                            "coupon_name":coupon_record_obj.coupon.name,
                            "coupon_type":coupon_record_obj.coupon.coupon_type,
                            "money_equivalent_value":coupon_record_obj.coupon.money_equivalent_value or "",
                            "off_percent":coupon_record_obj.coupon.off_percent or "",
                            "minimum_consume":coupon_record_obj.coupon.minimum_consume or "",
                            "related_course_id":coupon_record_obj.coupon.object_id or ""
                    }
                # 7.8 判断related_course_id所对应的值是否为空，如果为空，则说明是通用优惠券；如果不为空，则说明是课程专用优惠券
                    related_course_id_value = coupon_info.get('related_course_id')
                    if related_course_id_value and related_course_id_value == course_id:
                        course_coupon_vaule[coupon_record_obj.pk] = json.dumps(coupon_info)
                    if not related_course_id_value:
                        global_coupon_value[coupon_record_obj.pk] = json.dumps(coupon_info)
                # 7.9 将课程专用优惠券信息添加到course_account_value中
                course_account_value["course_coupon"] = json.dumps(course_coupon_vaule)
                # 7.10 将结算数据添加到Redis数据库中
                course_account_key = settings.COURSE_ACCOUNT_KEY.format(user_id,course_id)
                global_coupon_key = settings.GLOBAL_COUPON_KEY.format(user_id)
                self.conn.hmset(course_account_key,course_account_value)
                self.conn.hmset(global_coupon_key,global_coupon_value)
            response.data = "成功添加结算数据"

        except ObjectDoesNotExist as e:
            response.code = 1002
            response.error = '您所选的商品不存在！'

        except Exception as e:
            response.code = 1003
            response.error = str(e)

        return Response(response.dict)
