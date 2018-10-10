from rest_framework import serializers
from api.models import Course,CourseDetail


class CourseSerializer(serializers.ModelSerializer):
    # 课程难度等级
    level = serializers.SerializerMethodField()
    def get_level(self,obj):
        return obj.get_level_display()
    # 课程是否上线
    status = serializers.SerializerMethodField()
    def get_status(self,obj):
        return obj.get_status_display()
    # 课程价格
    price = serializers.SerializerMethodField()
    def get_price(self,obj):
        price_policy = obj.price_policy.all().first()
        return price_policy.price
    # 课程详细表的id
    courseDetailId = serializers.SerializerMethodField()
    def get_courseDetailId(self,obj):
        return obj.coursedetail.pk

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    # 课程名称
    course_name = serializers.SerializerMethodField()
    def get_course_name(self,obj):
        return obj.course.name
    # 推荐课程
    recommend_courses = serializers.SerializerMethodField()
    def get_recommend_courses(self,obj):
        recommend_courses_list = obj.recommend_courses.all()
        ret = []
        for recommend_course_obj in recommend_courses_list:
            ret.append({
                'recommendCourseDetailId':recommend_course_obj.coursedetail.pk,
                'recommendCcourseName':recommend_course_obj.name
            })
        return ret
    # 价格策略
    price_policy = serializers.SerializerMethodField()
    def get_price_policy(self,obj):
        price_policy_list = obj.course.price_policy.all()
        ret = []
        for price_policy_obj in price_policy_list:
            ret.append({
                'course_price':price_policy_obj.price,
                'valid_period':price_policy_obj.get_valid_period_display(),
            })
        return ret
    # 教师姓名
    teachers = serializers.SerializerMethodField()
    def get_teachers(self,obj):
        teachers_list = obj.teachers.all()
        ret = []
        for teacher_obj in teachers_list:
            ret.append({
                'teacher_name':teacher_obj.name,
                'teacher_brief':teacher_obj.brief,
            })
        return ret

    class Meta:
        model = CourseDetail
        fields = '__all__'
