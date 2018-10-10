from api.utils.serilizers import CourseDetailSerializer
from rest_framework.viewsets import ModelViewSet
from api.models import *


class CourseDetailView(ModelViewSet):
    '''课程详情视图是数据接口，需要用到视图类组件ModelViewSet'''
    queryset = CourseDetail.objects.all()
    serializer_class = CourseDetailSerializer