from django.contrib import admin
from api.models import *


admin.site.register(Course)
admin.site.register(CourseDetail)
admin.site.register(Teacher)
admin.site.register(PricePolicy)

admin.site.register(User)
admin.site.register(UserToken)

admin.site.register(Coupon)
admin.site.register(CouponRecord)