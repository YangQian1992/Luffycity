from django.db import models


# 课程分类表
class CourseCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32,verbose_name='课程分类')

    def __str__(self):
        return self.name


# 课程表
class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    cname = models.CharField(max_length=32,verbose_name='课程名称')
    # 课程表与课程分类表形成多对一关系
    category = models.ForeignKey(to='CourseCategory')

    def __str__(self):
        return self.cname


# 课程详情表
class CourseDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    course_overview = models.CharField(max_length=128,verbose_name='课程概述')
    scheduling = models.IntegerField(verbose_name='课程学时',null=True)
    course_difficulty = models.CharField(max_length=32,verbose_name='课程难度')
    number_of_students_studied = models.IntegerField(verbose_name='已学习人数')
    # 课程详情表与课程表形成一对一关系
    course = models.OneToOneField(to='Course')


