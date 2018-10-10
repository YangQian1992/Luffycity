from rest_framework.views import APIView
from rest_framework.response import Response
from luffycity_course.utils.serializers import *
from luffycity_course.models import *


class PythonCourse(APIView):
    def get(self,request):
        courseDetail_obj_list = CourseDetail.objects.filter(course__category__name='Python')
        courseDetail_serializer = CourseSerializer(courseDetail_obj_list,many=True)
        return Response(courseDetail_serializer.data)


class LinuxCourse(APIView):
    def get(self,request):
        courseDetail_obj_list = CourseDetail.objects.filter(course__category__name='Linux基础')
        courseDetail_serializer = CourseSerializer(courseDetail_obj_list,many=True)
        return Response(courseDetail_serializer.data)


class LuffycityAllCourse(APIView):
    def get(self,request):
        all_course_obj_list = CourseCategory.objects.all().values('course__cname','course__coursedetail__course_overview','course__coursedetail__number_of_students_studied','course__coursedetail__course_difficulty').distinct()
        return Response(all_course_obj_list)

