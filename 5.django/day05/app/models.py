from django.db import models


from django.db import models


class Grade(models.Model):

    # 创建一个班级
    g_name = models.CharField(max_length=10, unique=True, verbose_name='班级名称')

    class Meta:
        db_table = 'grade'


class Course(models.Model):
    c_name = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'course'


class StudentInfo(models.Model):
    # 电话号码
    phone = models.CharField(max_length=11, unique=True, null=True, verbose_name='手机号')

    # 地址
    address = models.CharField(max_length=50, null=True, verbose_name='家庭住址')

    class Meta:
        db_table = 'student_info'


# Create your models here.
class Student(models.Model):

    s_name = models.CharField(max_length=10, unique=True, verbose_name='姓名')

    s_age = models.IntegerField(default=16, verbose_name='年龄')

    s_sex = models.BooleanField(default=1, verbose_name='性别')

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 操作时间（对数据进行操作时的时间）
    operate_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # 数学成绩
    math = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    # 语文成绩
    chinese = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    # 一对一模型
    stu_info = models.OneToOneField(StudentInfo, null=True)

    # 一对多模型
    g = models.ForeignKey(Grade, null=True, on_delete=models.SET_NULL)

    # 多对多
    c = models.ManyToManyField(Course, null=True)

    class Meta:
        db_table = 'student'
