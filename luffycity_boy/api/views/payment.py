from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.authentications import Authentication
from api.utils.response import BaseResponse
from api.utils.myExceptions import CommonException
from django_redis import get_redis_connection
from django.conf import settings
from api.models import Course,CouponRecord,PricePolicy,Order,OrderDetail
from api.utils.pay import AliPay
import datetime
import time


class PaymentView(ViewSetMixin,APIView):
    '''
    支付接口 == 订单接口
    步骤：1、接收数据
          2、校验数据
          3、生成订单（默认未支付状态）
          4、调用支付宝的支付接口
                返回的post请求：修改订单，修改优惠券，修改贝里
                返回的get请求：查看订单状态
    '''
    authentication_classes = [Authentication]
    conn = get_redis_connection("default")

    def cal_favourable_price(self,original_price, coupon_record_obj):
        '''
        需求：通过课程的原价格和对应的课程优惠券来计算优惠后的价格
        :param original_price: 课程的原价格
        :param coupon_record_obj: 该课程所对应的优惠券
        :return: rebate_price：优惠后的价格
        '''
        # 获取该课程所对应的优惠券类型
        coupon_type = coupon_record_obj.coupon.coupon_type
        # 根据不同的优惠券类型进行计算优惠后的价格
        if coupon_type == 0:  # 立减券
            money_equivalent_value = coupon_record_obj.coupon.money_equivalent_value
            rebate_price = original_price - money_equivalent_value
            if rebate_price < 0:
                rebate_price = 0
        elif coupon_type == 1:  # 满减券
            minimum_consume = coupon_record_obj.coupon.minimum_consume
            if original_price > minimum_consume:
                money_equivalent_value = coupon_record_obj.coupon.money_equivalent_value
                rebate_price = original_price - money_equivalent_value
            else:
                raise CommonException("优惠券不符合条件！", 1008)
        elif coupon_type == 2:  # 折扣券
            off_percent = coupon_record_obj.coupon.off_percent
            rebate_price = original_price * (off_percent / 100)
        else:  # 不使用优惠券
            rebate_price = original_price
        return rebate_price

    def ali(self):
        # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
        app_id = "2016091100486897"
        # POST请求，用于最后的检测
        notify_url = "http://47.94.172.250:8804/page2/"
        # notify_url = "http://www.wupeiqi.com:8804/page2/"
        # GET请求，用于页面的跳转展示
        return_url = "http://47.94.172.250:8804/page2/"
        # return_url = "http://www.wupeiqi.com:8804/page2/"
        merchant_private_key_path = "api/keys/app_private_2048.txt"
        alipay_public_key_path = "api/keys/alipay_public_2048.txt"
        alipay = AliPay(
            appid=app_id,
            app_notify_url=notify_url,
            return_url=return_url,
            app_private_key_path=merchant_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            debug=True,  # 默认False,
        )
        return alipay

    def create(self,request,*args,**kwargs):
        '''
        需求：用户点击“立即支付”，将结算中的商品添加到订单中
        方案：前端将结算中的商品信息通过POST请求发送到后端 --> 前端请求发送过来的数据结构如下：
            {
                "courses":{
                    1:{
                        "choose_price_id":1,
                        "coupon_record_id":2
                    },
                    2:{
                        "choose_price_id":4,
                        "coupon_record_id":3
                    }
                },
                "global_coupon_id":2,
                "beili":1000,
                "total_money":2000
            };
              后端获取到数据，对数据进行校验成功后，将其添加到订单中。
            计算价格的优先级如下：
              （课程1的原价格*课程1的优惠券+课程2的原价格*课程2的优惠券）* 通用优惠券 - 贝里/10

            code: 1100 --> 普通错误
                  1000 --> 响应成功
                  1001 --> 贝里数有问题
                  1002 --> 课程不存在
                  1003 --> 课程未上线或者已下线
                  1004 --> 价格策略有问题
                  1005 --> 课程优惠券有问题
                  1006 --> 课程优惠券与课程不匹配
                  1007 --> 课程优惠券与课程不匹配
                  1008 --> 优惠券不符合条件
                  1009 --> 通用优惠券有问题
                  1010 --> 支付价格有问题
        '''
        response = BaseResponse()
        try:
            # 1. 清空当前用户结算中心的数据(例如：global_coupon_1，course_account_1_4)
            keys_list = self.conn.keys(settings.COURSE_ACCOUNT_KEY.format(request.user.pk,'*'))
            keys_list.append(settings.GLOBAL_COUPON_KEY.format(request.user.pk))
            self.conn.delete(*keys_list)

            # 2. 获取前端发送过来的数据
            user_obj = request.user
            courses_dict = request.data.get("courses")
            global_coupon_id = request.data.get("global_coupon_id")
            beili = int(request.data.get("beili"))
            total_money = request.data.get("total_money")

            # 3. 校验前端发送过来的数据
            coupon_use_time = datetime.datetime.now()
            course_price_list = []
            # 3.1 校验贝里数是否在登录用户实际拥有范围内
            if user_obj.beili < beili:
                raise CommonException("贝里数有问题！",1001)
            # 3.2 校验课程信息
            for course_pk,course_info in courses_dict.items():
                # 3.2.1 校验课程是否存在
                course_obj = Course.objects.filter(pk=int(course_pk)).first()
                if not course_obj:
                    raise CommonException("课程不存在！",1002)
                if course_obj.status != 0:
                    raise CommonException("课程未上线或者已下线！",1003)
                # 3.2.2 校验价格策略是否存在
                choose_price_id = course_info.get("choose_price_id")
                price_policy_queryset = course_obj.price_policy.all()
                if choose_price_id not in [price_policy_obj.pk for price_policy_obj in price_policy_queryset]:
                    raise CommonException("价格策略有问题！",1004)
                # 3.2.3 校验课程优惠券是否存在
                coupon_record_id = course_info.get("coupon_record_id")
                coupon_record_obj = CouponRecord.objects.filter(
                    pk=coupon_record_id,
                    user=user_obj,
                    status=0,
                    coupon__valid_begin_date__lt=coupon_use_time,
                    coupon__valid_end_date__gt=coupon_use_time
                ).first()
                if not coupon_record_obj:
                    raise CommonException("课程优惠券有问题！",1005)
                related_course_obj = coupon_record_obj.coupon.content_object
                if course_obj != related_course_obj:
                    raise CommonException("课程优惠券与课程不匹配！",1006)

                # 3.2.4 计算优惠后的价格
                original_price = PricePolicy.objects.filter(pk=choose_price_id).first().price
                rebate_price = self.cal_favourable_price(original_price,coupon_record_obj)
                course_price_list.append(rebate_price)
            # 3.3 校验通用优惠券合法性
            global_coupon_record_obj = CouponRecord.objects.filter(
                pk=global_coupon_id,
                user=user_obj,
                status=0,
                coupon__valid_begin_date__lt=coupon_use_time,
                coupon__valid_end_date__gt=coupon_use_time
            ).first()
            if not global_coupon_record_obj:
                raise CommonException("通用优惠券有问题！",1009)
            # 3.4 校验最终价格是否一致
            favourable_price = self.cal_favourable_price(sum(course_price_list),global_coupon_record_obj)
            final_price = favourable_price - beili/10
            if final_price < 0:
                final_price = 0
            if total_money != final_price:
                raise CommonException("支付价格有问题！",1010)

            # 4. 生成订单（默认未支付状态）
            order_obj = Order.objects.create(
                user=user_obj,
                actual_amount=final_price,
                payment_type=1,
                status=1
            )
            for course_pk, course_info in courses_dict.items():
                choose_price_id = course_info.get("choose_price_id")
                original_price = PricePolicy.objects.filter(pk=choose_price_id).first().price
                coupon_record_id = course_info.get("coupon_record_id")
                coupon_record_obj = CouponRecord.objects.filter(
                    pk=coupon_record_id,
                    user=user_obj,
                    status=0,
                    coupon__valid_begin_date__lt=coupon_use_time,
                    coupon__valid_end_date__gt=coupon_use_time
                ).first()
                rebate_price = self.cal_favourable_price(original_price, coupon_record_obj)
                valid_period = PricePolicy.objects.filter(pk=choose_price_id).first().get_valid_period_display()
                OrderDetail.objects.create(
                    original_price=original_price,
                    price=rebate_price,
                    valid_period_display=valid_period,
                    order=order_obj,
                    content_type_id=11,
                    object_id=int(course_pk)
                )
                response.data = "成功生成订单！"
            # 5. 调用支付接口
            alipay = self.ali()
            # 生成支付的url
            query_params = alipay.direct_pay(
                subject="路飞学城",  # 商品简单描述
                out_trade_no="x2" + str(time.time()),  # 商户订单号
                total_amount=round(final_price,2),  # 交易金额(单位: 元 保留俩位小数)
            )
            pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
            response.pay_url = pay_url

            # 6. 支付成功后通过POST请求访问notify_url：
                # 6.1 更改订单
                # 6.2 更改优惠券
                # 6.3 更改贝里数
            # 7. 修改完后通过GET请求访问return_url,用于页面的跳转展示。

        except CommonException as e:
            response.code = e.code
            response.error = e.error

        return Response(response.dict)


