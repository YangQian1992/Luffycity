from api.utils.serilizers import CourseSerializer
from rest_framework.viewsets import ModelViewSet
from api.models import *


class CourseView(ModelViewSet):
    '''课程视图是数据接口，需要用到视图类组件ModelViewSet'''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


