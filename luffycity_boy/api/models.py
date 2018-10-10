from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType


# 登录认证相关的表
class User(models.Model):
    '''用户表'''
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    type_choice = ((1,'VIP'),(2,'SVIP'),(3,'SSSVIP'))
    type = models.IntegerField(choices=type_choice)
    beili = models.IntegerField(default=100)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class UserToken(models.Model):
    '''用户Token表'''
    userToken = models.CharField(max_length=128)
    # 用户Token表与用户表建立一对一的关系
    user = models.OneToOneField(to='User',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户Token表'
        verbose_name_plural = '用户Token表'


# 课程相关的表
class Course(models.Model):
    '''专题课程'''
    name = models.CharField(max_length=128,unique=True)
    course_img = models.CharField(max_length=255)
    brief = models.TextField(verbose_name='课程概况',max_length=2048)

    level_choices = ((0,'初级'),(1,'中级'),(2,'高级'))
    level = models.SmallIntegerField(choices=level_choices,default=1)
    pub_date = models.DateField(verbose_name='发布日期',blank=True,null=True)
    period = models.PositiveIntegerField(verbose_name='建议学习周期（days）',default=7)
    order = models.IntegerField('课程顺序',help_text='从上一个课程数字往后排')

    status_choices = ((0,'上线'),(1,'下线'),(2,'预上线'))
    status = models.SmallIntegerField(choices=status_choices,default=0)

    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    price_policy = GenericRelation(to='PricePolicy')    # 价格策略
    coupons = GenericRelation(to='Coupon')  # 优惠券生成规则
    order_detail = GenericRelation(to='OrderDetail')    # 订单详情

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '专题课程'
        verbose_name_plural = '专题课程'


class CourseDetail(models.Model):
    '''课程详情页内容'''
    course = models.OneToOneField(to='Course',on_delete=models.CASCADE)
    hours = models.IntegerField('课时')
    # 课程的标语 口号
    course_slogan = models.CharField(max_length=125,blank=True,null=True)
    # video_brief_link = models.CharField(verbose_name='课程介绍',max_length=255,blank=True,null=True)
    # why_study = models.TextField(verbose_name='为什么学习这门课程')
    # what_to_study_brief = models.TextField(verbose_name='我将学到哪些内容')
    # career_improvement = models.TextField(verbose_name='此项目如何有助于我的职业生涯')
    # prerequisite = models.TextField(verbose_name='课程选修要求',max_length=1024)

    # 推荐课程
    recommend_courses = models.ManyToManyField(to='Course',related_name='recommend_by',blank=True)

    teachers = models.ManyToManyField(to='Teacher',verbose_name='课程讲师')

    def __str__(self):
        return '%s' % self.course

    class Meta:
        verbose_name = '课程详情'
        verbose_name_plural = '课程详情'


class Teacher(models.Model):
    '''教师表'''
    name = models.CharField(max_length=32)
    image = models.CharField(max_length=128)
    brief = models.TextField(max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '教师表'
        verbose_name_plural = '教师表'


class PricePolicy(models.Model):
    '''价格与课程有效期表'''
    price = models.FloatField()

    valid_period_choices = (
        (1,'1天'),
        (3,'3天'),
        (7,'1周'),
        (14,'2周'),
        (30,'1个月'),
        (60,'2个月'),
        (90,'3个月'),
        (180,'6个月'),
        (210,'12个月'),
        (540,'18个月'),
        (720,'24个月'),
    )
    valid_period = models.SmallIntegerField(choices=valid_period_choices)

    # 建立ContentType 表关系
        # 第一步：生成ForeignKey字段关联ContentType
    content_type = models.ForeignKey(to=ContentType,on_delete=models.CASCADE)
        # 第二步：生成一个IntergerField 字段关联
    object_id = models.PositiveIntegerField()
        # 第三步：生成一个GenericForeignKey 把上面的两个字段注册进去
    content_object = GenericForeignKey('content_type','object_id')

    def __str__(self):
        return '%s(%s)%s' % (self.content_object,self.get_valid_period_display(),self.price)

    class Meta:
        # 联合唯一
        unique_together = ('content_type','object_id','valid_period')
        verbose_name = '价格策略'
        verbose_name_plural = '价格策略'


# 优惠券相关的表
class Coupon(models.Model):
    '''优惠券生成规则表'''
    name = models.CharField(max_length=64,verbose_name='优惠券名称')
    brief = models.TextField(blank=True,null=True,verbose_name='优惠活动介绍')

    coupon_type_choice = ((0,'立减券'),(1,'满减券'),(2,'折扣券'))
    coupon_type = models.SmallIntegerField(choices=coupon_type_choice,default=0,verbose_name='优惠券类型')

    money_equivalent_value = models.IntegerField(verbose_name='等值货币',blank=True,default=0)
    off_percent = models.PositiveIntegerField(verbose_name='折扣百分比',help_text='只针对折扣券，例7.9折，写79',blank=True,null=True)
    minimum_consume = models.PositiveIntegerField(verbose_name='最低消费',default=0,help_text='仅在满减券时填写此字段')

    content_type = models.ForeignKey(ContentType,blank=True,null=True)
    object_id = models.PositiveIntegerField(verbose_name='绑定课程',blank=True,null=True,help_text='可以把优惠券跟课程绑定')
    content_object = GenericForeignKey('content_type','object_id')

    quantity = models.PositiveIntegerField(verbose_name="数量（张）",default=1)
    open_date = models.DateField(verbose_name='优惠券领取开始时间')
    close_date = models.DateField(verbose_name='优惠券领取结束时间')
    valid_begin_date = models.DateField(verbose_name='有效期开始时间',blank=True,null=True)
    valid_end_date = models.DateField(verbose_name='有效期结束时间',blank=True,null=True)

    # 将生成的优惠券规则添加到数据库的日期时间
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '优惠券生成规则'
        verbose_name_plural = '优惠券生成规则'

    def __str__(self):
        return '{}({})'.format(self.get_coupon_type_display(),self.name)


class CouponRecord(models.Model):
    '''优惠券记录'''
    coupon = models.ForeignKey(to='Coupon',on_delete=models.CASCADE,verbose_name='优惠券生成规则')
    user = models.ForeignKey(to='User',verbose_name='优惠券的拥有者')

    status_choices = ((0,'未使用'),(1,'已使用'),(2,'已过期'))
    status = models.SmallIntegerField(choices=status_choices,default=0,verbose_name='优惠券使用状态')
    get_time = models.DateTimeField(verbose_name='优惠券领取时间',help_text='用户领取时间')
    used_time = models.DateTimeField(verbose_name='优惠券使用时间',blank=True,null=True)
    order_id = models.IntegerField(verbose_name='关联订单ID',blank=True,null=True)

    class Meta:
        verbose_name = '优惠券记录'
        verbose_name_plural = '优惠券记录'

    def __str__(self):
        return '{}-{}'.format(self.user,self.coupon)


# 订单相关的表
class Order(models.Model):
    '''订单表'''
    payment_type_choice = ((0,'微信'),(1,'支付宝'),(2,'优惠码'),(3,'贝里'))
    payment_type = models.SmallIntegerField(choices=payment_type_choice)
    payment_number = models.CharField(max_length=128,verbose_name='支付宝第三方订单号',null=True,blank=True)
    order_number = models.CharField(max_length=128,verbose_name='订单号',unique=True,null=True,blank=True)  # 考虑到订单合并支付的问题
    actual_amount = models.FloatField(verbose_name='实际支付金额')
    status_choices = ((0,'交易成功'),(1,'待支付'),(2,'退费申请中'),(3,'已退费'),(4,'主动取消'),(5,'超时取消'))
    status = models.SmallIntegerField(choices=status_choices,verbose_name='交易状态')
    date = models.DateTimeField(auto_now_add=True,verbose_name='订单生成时间')
    pay_time = models.DateTimeField(blank=True,null=True,verbose_name='订单付款时间')
    cancel_time = models.DateTimeField(blank=True,null=True,verbose_name='订单取消时间')

    # 订单与用户建立多对一的关系
    user = models.ForeignKey(to='User')

    class Meta:
        verbose_name = '订单表'
        verbose_name_plural = '订单表'

    def __str__(self):
        return '{}'.format(self.order_number)


class OrderDetail(models.Model):
    '''订单详情'''
    original_price = models.FloatField(verbose_name='课程原价')
    price = models.FloatField(verbose_name='折后价格')
    valid_period_display = models.CharField(max_length=32,verbose_name='有效期显示') # 在订单页显示
    valid_period = models.PositiveIntegerField(verbose_name='有效期（days）',null=True,blank=True)    # 课程有效期
    content = models.CharField(max_length=255,blank=True,null=True)
    memo = models.CharField(max_length=255,blank=True,null=True)

    order = models.ForeignKey('Order')  # 与订单表建立多对一的关系

    content_type = models.ForeignKey(to=ContentType)  # 可关联普通课程或学位课程
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    class Meta:
        verbose_name = '订单详情'
        verbose_name_plural = '订单详情'
        unique_together = ('order','content_type','object_id')

    def __str__(self):
        return '{}-{}-{}'.format(self.order,self.content_type,self.price)

