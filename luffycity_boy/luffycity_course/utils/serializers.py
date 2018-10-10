from luffycity_course.models import *
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = "__all__"
        extra_kwargs = {"course":{"write_only":True}}
    # 查询表中的一对多字段
    course_name = serializers.CharField(max_length=32, source="course.cname",read_only=True)


