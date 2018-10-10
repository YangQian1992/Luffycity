"""luffycity_boy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views as app01_views
from luffycity_course import views as luffycity_views

from rest_framework import routers
from api.views.course import CourseView
from api.views.course_detail import CourseDetailView
from api.views.login import LoginView
from api.views.shopping_cart import ShoppingCartView
from api.views.course_account import CourseAccountView
from api.views.payment import PaymentView

# 数据接口
router = routers.DefaultRouter()
router.register('courses',CourseView)
router.register('course_detail',CourseDetailView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^luffycity/', app01_views.Luffycity.as_view()),
    url(r'^login/', app01_views.Login.as_view()),
    ##### DRF 给前端传json数据的视图 #####
    url(r'^python_course/', luffycity_views.PythonCourse.as_view()),
    url(r'^linux_course/', luffycity_views.LinuxCourse.as_view()),
    url(r'^luffycity_all_course/', luffycity_views.LuffycityAllCourse.as_view()),

    ##### vue-cli 做的luffycity_girl 前端单页面 #####
    url(r'^',include(router.urls)), # 免费课程/课程详情等视图的数据接口
    url(r'^api/login/$',LoginView.as_view()),   # 登录校验视图的逻辑接口
    url(r'^shopping_cart/$',ShoppingCartView.as_view({'get':'list','post':'create'})),   # 购物车视图的接口（增查需要手动写）
    url(r'^shopping_cart/(?P<pk>\d+)/$',ShoppingCartView.as_view({'put':'update','delete':'destroy'})),   # 购物车视图的接口（删改需要手动写）
    url(r'^course_account/$', CourseAccountView.as_view({'get': 'list', 'post': 'create'})),  # 商品结算视图的接口（增查需要手动写）
    url(r'^course_account/(?P<pk>\d+)/$', CourseAccountView.as_view({'put': 'update'})),  # 商品结算视图的接口（改需要手动写）
    url(r'^payment/$', PaymentView.as_view({'post': 'create'})),  # 商品订单视图的接口（增查需要手动写）
    url(r'^payment/(?P<pk>\d+)/$', PaymentView.as_view({'put': 'update'})),  # 商品订单视图的接口（改需要手动写）
]
