
from flask import Blueprint, render_template, request

from sqlalchemy import or_, not_

from user.models import db, Students, Grade, Course

# 创建蓝图
user_blueprint = Blueprint('app', __name__)


# 创建一个路由控制
@user_blueprint.route('/', methods=['GET'])
def hello():
    return 'hello'


@user_blueprint.route('/create_db/')
def create_db():
    # 用于初次创建models中所有的表
    db.create_all()
    return '创建成功'


@user_blueprint.route('/drop_db/')
def drop_db():
    # 删除models中所有的表
    db.drop_all()
    return '删除成功'


@user_blueprint.route('/create_stu/')
def create_stu():
    # 实现学生对象的创建
    stu = Students()
    stu.s_name = '小明'
    stu.save()
    return '创建学生信息成功'


@user_blueprint.route('/create_stu_all/')
def create_stu_all():
    # 批量创建，add_all()
    names = ['小王', '老王', '厂长', '李哥', '小花']
    stu_list = []
    for name in names:
        stu = Students()
        stu.s_name = name
        # stu.save()
        # db.session.add(stu)
        stu_list.append(stu)
    db.session.add_all(stu_list)
    db.session.commit()
    return '批量创建学生信息成功'


@user_blueprint.route('/sel_stu/')
def sel_stu():
    # 查询, filter(), filter_by()
    # 返回类型是querybase
    stu = Students.query.filter(Students.s_name == '厂长').first()
    # all(),first()
    stu = Students.query.filter_by(s_name='小明明').first()
    stus = Students.query.all()
    # 执行sql
    sql = 'select * from students;'
    stus = db.session.execute(sql)

    # 模糊查询，名字中有’小‘的
    # select * from students where s_name like '%王%'
    # select * from students where s_name like '王%'
    # select * from students where s_name like '_王%'
    stus = Students.query.filter(Students.s_name.contains('小'))
    stus = Students.query.filter(Students.s_name.startswith('小'))

    # 查询id在某个范围之内的学生信息
    # select * from students where id in (2,3,4,5)
    stus = Students.query.filter(Students.id.in_([2,3,4,5]))

    # 查询年龄大哟18的学生信息
    stus = Students.query.filter(Students.s_age > 18)
    stus = Students.query.filter(Students.s_age.__gt__(18))

    # 查询id=4的学生信息
    # get()获取主键对应的行数据
    stu = Students.query.get(4)

    # offset+limit
    stus = Students.query.limit(3)
    stus = Students.query.offset(3).limit(3)

    # order_by()
    stus = Students.query.order_by('-id')
    stus = Students.query.order_by('id')

    # 查询姓名中包含’小‘，并且年龄=18
    stus = Students.query.filter(Students.s_name.contains('小'), Students.s_age == 18)

    # # 查询姓名中包含’小‘，或年龄=18
    # django中：filter(Q(A) | Q(B))
    # flask中：filter(or_(A, B))
    stus = Students.query.filter(or_(Students.s_name.contains('小'), Students.s_age == 18))

    # 查询姓名中不包含王，且年龄等于18的
    stus = Students.query.filter(not_(Students.s_name.contains('王')), Students.s_age == 18)

    return '查询成功'


@user_blueprint.route('/delete_stu/<int:id>/')
def delete_stu(id):
    # 删除
    stu = Students.query.filter(Students.id == id).first()
    if stu:
        db.session.delete(stu)
        db.session.commit()
        return '删除成功'
    else:
        return '该id不存在，请重新输入'


@user_blueprint.route('/update_stu/<int:id>/')
def update_stu(id):
    # 修改
    stu = Students.query.filter_by(id=id).first()
    stu.s_name = '哈哈哈'
    stu.s_age = 22
    stu.save()
    return '修改成功'


# 实现分页
@user_blueprint.route('/paginate/', methods=['GET', 'POST'])
def stu_page():
    page = int(request.args.get('page', 1))
    # 1.offset+limit
    stus = Students.query.offset((page - 1) * 2).limit(2)
    # 2.切片
    stus = Students.query.all()[((page - 1) * 2):(page * 2)]
    # 3.sql
    sql = 'select * from students limit %s,%s' % (((page - 1) * 2), (page * 2))
    stus = db.session.execute(sql)
    # 4.paginate()方法
    paginate = Students.query.paginate(page, 2)
    stus = paginate.items
    return render_template('index.html', stus=stus, paginate=paginate)


# 一对多关联关系数据的操作
@user_blueprint.route('/create_grade/', methods=['GET', 'POST'])
def create_grade():
    names = ['java', 'python', 'html5', 'php', 'c']
    grade_list = []
    for name in names:
        grade = Grade()
        grade.g_name = name
        grade_list.append(grade)
    db.session.add_all(grade_list)
    db.session.commit()
    return '班级添加成功'


@user_blueprint.route('/rel_stu_grade/')
def rel_stu_grade():
    stus_ids = [2, 3, 4]
    for id in stus_ids:
        stu = Students.query.get(id)
        # 在flask中， stu.s_g获取的值为int类型
        # 在django中， stu.s_g获取的是对象，stu.s_g_id获取到的int类型。
        stu.s_g = 1
        stu.save()
    return '关联学生和班级'


@user_blueprint.route('/create_stu_gra/')
def create_stu_gra():
    stu = Students()
    stu.s_name = '李哥'
    stu.s_age = 27
    stu.s_g = 3
    stu.save()
    return '一对多一个学生添加成功'


@user_blueprint.route('/create_stus_gra/')
def create_stus_gra():
    names = ['老王', '55开', 'uzi', '大哥', '麻辣香锅', 'god', 'wawa']
    stu_list = []
    i = 1
    for name in names:
        stu = Students()
        stu.s_name = name
        stu.s_g = i % 5 + 1
        i += 1
        stu_list.append(stu)
    db.session.add_all(stu_list)
    db.session.commit()
    return '一对多批量学生添加成功'


# 通过一对多关联关系相互查询
@user_blueprint.route('/sel_stu_by_grade/')
def sel_stu_by_grade():
    # 通过班级查找学生
    grade = Grade.query.filter(Grade.g_name == 'python').first()
    # 获取到班级对应的学生信息
    stus = grade.students
    return '通过班级查找学生成功'


@user_blueprint.route('/sel_grade_by_stu/')
def sel_grade_by_stu():
    # 通过学生查找班级
    stu = Students.query.get(6)
    # 获取到学生对应的班级信息
    grade = stu.grade
    return '通过学生查找班级成功'


# 多对多关联关系
@user_blueprint.route('/create_course/')
def create_course():
    names = ['语文', '数学', '英语', '物理']
    for name in names:
        course = Course()
        course.c_name = name
        db.session.add(course)
    db.session.commit()
    return '添加成功'


@user_blueprint.route('/add_stu_cou/')
def add_stu_cou():
    stu = Students.query.get(1)
    # 学生对象查找课程信息， stu.cou
    cou1 = Course.query.get(1)
    cou2 = Course.query.get(2)
    cou3 = Course.query.get(3)
    cou4 = Course.query.get(4)
    # 绑定学生和课程的关联关系
    stu.cou.append(cou1)
    stu.cou.append(cou2)
    stu.cou.append(cou3)
    stu.cou.append(cou4)

    stu.save()
    return '小明选课成功'