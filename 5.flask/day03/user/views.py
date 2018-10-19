
from flask import Blueprint

from sqlalchemy import or_, not_

from user.models import db, Students

# 创建蓝图
user_blueprint = Blueprint('app', __name__)


# 创建一个路由控制
@user_blueprint.route('/', methods=['GET'])
def hello():
    return 'hello'


@user_blueprint.route('/create_db/')
def create_de():
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


