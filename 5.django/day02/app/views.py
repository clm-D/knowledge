from django.db.models import Q, F, Avg
from django.http import HttpResponse
from django.shortcuts import render

from app.models import Student, StudentInfo, Grade, Course


# Create your views here.
def create_stu(request):

    # 创建学生信息
    # 引入ORM概念：对象关系映射
    # 第一种方式
    Student.objects.create(s_name='xxx')
    Student.objects.create(s_name='xxx1')
    Student.objects.create(s_name='xxx2')
    Student.objects.create(s_name='xxx3')

    # 第二种方法
    # stu = Student()
    # stu.s_name = 'xm'
    # stu.save()

    #第三种
    # stu = Student('sm', 18, 1)
    # stu.save()


    return HttpResponse('创建学生方法')


def select_stu(request):

    """
    all: 查询所有
    filter: 获取的结果为queryset,可以返回空，一条或多条数据。
    get: 获取的结果时object对象，如果获取不成功，会报错；如果获取多条数据，也会报错。
    exclude： 不包含
    order_by(): 排序
    """
    # 查询数据
    # all()获取全部
    # select * from student;
    stus = Student.objects.all()
    # filter()条件查询,存在就返回对应值，不存在就返回空
    # select * from student where s_name='sm'
    stus = Student.objects.filter(s_name='sm')
    stu_names = [stu.s_name for stu in stus]
    print(stu_names)

    # get():条件查询，只查询一个，如果有多个就报错
    stus = Student.objects.get(s_age=19)


    # 多条件查询
    # select * from student where s_name='sm' and s_age=16
    stus = Student.objects.filter(s_age=16).filter(s_name='sm')
    stus = Student.objects.filter(s_age=16, s_name='sm')


    # 查询不等于的
    # select * from student where s_namg<>'sm'
    stus = Student.objects.exclude(s_name='sm')


    # 查询并排序,升降
    # select * from student order by id;
    stus = Student.objects.all().order_by('id')  # 升序
    stus = Student.objects.all().order_by('-id')  # 降序


    # values()
    # stus = Student.objects.all().values('id', 's_name', 's_age', 's_sex')
    # return HttpResponse(stus)


    # get(), first()
    # stus = Student.objects.get(id=1)
    stus = Student.objects.filter(id=1).first()

    # last(), first()
    stus = Student.objects.all().order_by('id').first()  # 升序
    stus = Student.objects.all().order_by('-id').last()  # 降序

    stus = Student.objects.all().order_by('id')[1]  # 升序

    # return HttpResponse(stus.id)


    # 其它条件查询
    # select * from student where s_name like '%m%'
    stus = Student.objects.filter(s_name__icontains='m')
    # select * from student where s_name like 'm%'
    stus = Student.objects.filter(s_name__startswith='m')
    # select * from student where s_name like '%m'
    stus = Student.objects.filter(s_name__endswith='m')

    # in
    # select * from student where id in (1,2)
    stus = Student.objects.filter(id__in=[1,2])

    # gt,gte 大于，大于等于   lt,lte  小于，小于等于
    stus = Student.objects.filter(s_age__lt=17)

    # pk
    stus = Student.objects.filter(id=1)
    stus = Student.objects.filter(pk=1)

    # Q(),查询姓名叫‘xm’的 或者年龄等于18的
    stus = Student.objects.filter(Q(s_name='xm') | Q(s_age=18))
    # 与 &
    stus = Student.objects.filter(Q(s_name='xm') & Q(s_age=18))
    # 非 ~
    stus = Student.objects.filter(~Q(s_name='xm') | Q(s_age=18))

    # F()
    # 查询语文成绩比数学成绩低10分的学生信息
    # seelct * from student where math - 10 > chinses
    stus = Student.objects.filter(math__gt=F('chinese') + 10)

    # 求数学成绩的平均值
    avg_math = Student.objects.aggregate(Avg('math'))


    # 获取学生的姓名
    stu_names = [(stu.s_name,stu.id) for stu in stus]
    print(stu_names)
    # print(stus)

    print(avg_math)
    return HttpResponse(stu_names)


def delete_stu(request):
    # 删除
    stu = Student.objects.get(pk=6)
    stu.delete()

    Student.objects.filter(id=2).first().delete()

    return HttpResponse('删除')


def update_stu(request):
    # 更新
    # 第一种
    stu = Student.objects.get(pk=1)
    stu.s_name = '3x'
    stu.save()

    # 第二种
    Student.objects.filter(id=1).update(s_name='哈哈')

    return HttpResponse('修改')



def create_stu_info(request):

    if request.method == 'GET':
        # 创建学生信息的拓展数据
        StudentInfo.objects.create(phone='18200384770', address='成都')
        StudentInfo.objects.create(phone='18267893456', address='北京')
        StudentInfo.objects.create(phone='15777778888', address='上海')
        StudentInfo.objects.create(phone='13566669999', address='重庆')

        return HttpResponse('创建学生拓展信息')


    if request.method == 'POST':
        pass


def stu_add_stuinfo(request):

    if request.method == 'GET':
        # 给id为1的学生添加拓展表中id=2的信息，
        stu1 = Student.objects.get(id=1)
        # 绑定关系方法 1
        stu1.stu_info_id = 1
        stu1.save()

        # 绑定关系方法 2
        stu2 = Student.objects.get(id=2)
        stu2.stu_info = StudentInfo.objects.get(id=2)
        stu2.save()


        stu3 = Student.objects.get(id=3)
        stu3.stu_info_id = 3
        stu3.save()

        return HttpResponse('绑定学生信息')


def sel_phone_by_stu(request):

    if request.method == 'GET':
        # 获取id=2的学生的手机号
        # 方法1：
        stu = Student.objects.filter(id=2)
        info_id = stu.stu_info_id
        stu_info = StudentInfo.objects.get(id=info_id)
        phone = stu_info.phone

        # 方法2：
        stu = Student.objects.get(id=2)
        stu_info = stu.stu_info
        phone = stu_info.phone

        print(phone)

        return HttpResponse('通过学生查手机号')



def sel_stu_by_phone(request):

    if request.method == 'GET':
        # 通过手机号查学生 15777778888
        stu_info = StudentInfo.objects.get(phone='15777778888')
        # stu_info.student和stu_info.stu只能用一个
        stu = stu_info.stu
        s_name = stu.s_name
        print(s_name)

        return HttpResponse('通过手机号查学生信息')



def create_grade(request):
    # 创建班级
    if request.method == 'GET':
        Grade.objects.create(g_name='py1805')
        Grade.objects.create(g_name='py1804')
        Grade.objects.create(g_name='py1803')
        Grade.objects.create(g_name='py1802')
        Grade.objects.create(g_name='py1801')

        return HttpResponse('创建班级')


def sel_grade_by_stu(request):
    # 班级与学生对查
    if request.method == 'GET':
        # 查询叫sm的学生对应的班级
        stu = Student.objects.get(s_name='sm')
        grade = stu.g
        g_name = grade.g_name
        print(g_name)

        # 查询py1805班的学生人数和姓名
        grades = Grade.objects.get(g_name='py1805')
        # grades.student_set.all()和grades.stu.all()只能用一个
        stus = grades.stu.all()

        # 获取学生的姓名
        stu_names = [stu.s_name for stu in stus]
        print(stu_names)
        print(len(stus))

        return HttpResponse('查询成功')


def create_course(request):
    # 添加课程信息
    if request.method == 'GET':
        courses = ['java', 'python', 'c++', 'h5', 'c']
        for name in courses:
            Course.objects.create(c_name=name)

        return HttpResponse('课程创建成功')


def create_stu_course(request):
    # 创建学生与课程的对应关系
    if request.method == 'GET':
        # 添加学生对应的课程信息
        # 让id=2的学生选择课程（id=1，2）
        stu = Student.objects.get(id=2)
        # 添加add()方法
        stu.c.add(1)
        stu.c.add(2)

        # 添加课程c++的和学生id=1，4的关系
        cour = Course.objects.get(c_name='c++')

        # 添加add()
        cour.student_set.add(1)
        cour.student_set.add(4)

        # 删除id=2的学生选的id=2的课程
        stu.c.remove(2)


        return HttpResponse('创建学生与课程关系成功')
