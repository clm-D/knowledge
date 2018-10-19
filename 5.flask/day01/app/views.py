
from flask import Blueprint, redirect, url_for,\
    request, make_response, render_template, abort,\
    session

from utils.functions import is_login

# 第一步，创建蓝图blue并使用其去管理路由（别名app）
blue = Blueprint('app', __name__)


@blue.route('/')
@is_login
def hello_world():
    return 'Hello World!'


# 路由匹配规则
# 1.<id>: 默认接收的类型为str
# 2.<string:id>: 指定id的类型为字符串str
# 3.<int:id>: 指定id的类型为整型int
# 4.<float:id>: 指定id的类型为浮点数float
# 5.<path:upath>: 指定接收的path为URL中的路径


@blue.route('/get_id/<id>/', methods=['GET'])
def get_id(id):
    # 匹配str类型的id值
    return 'id: %s' % id


@blue.route('/get_int_id/<int:id>/')
def get_int_id(id):
    # 匹配int类型的id值
    return 'id: %d' % id


@blue.route('/get_float_id/<float:id>/')
def get_float_id(id):
    # 匹配float类型的值，不能匹配int类型的
    return 'id: %.2f' % id


@blue.route('/get_path/<path:upath>/')
def get_path(upath):
    # 匹配URL路径,匹配/get_path/后面的所有
    return 'path: %s' % upath


@blue.route('/redirect/')
def redirect_hello():
    # 实现跳转
    # 1.硬编码URL
    # 2.反向解析redirect(url_for('蓝图别名.跳转的函数名'))
    # return redirect('/app/')
    # return redirect(url_for('app.hello_world'))
    return redirect(url_for('app.get_id', id=5))


@blue.route('/request/', methods=['GET', 'POST', 'PUT'])
def get_request():
    # 请求上下文 request
    # 获取GET请求传递的参数：request.args.get(key)/request.args.getlist(key)
    # 获取POST、PUT、PATCH、DELETE请求传递的参数：request.form.get(key)/request.form.getlist(key)
    # 判断HTTP请求方式： request.method
    pass


@blue.route('/response/', methods=['GET'])
def get_response():
    # 创建响应
    # res = make_response('人生苦短，我用Python', 200)
    # 响应绑定cookie, set_cookie(key, value, max_age, explres)
    # 删除cookie, delete_cookie(key)
    res_index = render_template('index.html')
    res = make_response(res_index, 200)
    return res


@blue.route('/index/', methods=['GET'])
def index():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    try:
        a/b
    except Exception as e:
        print(e)
        # 抛出错误
        abort(500)
    return render_template('index.html')


@blue.errorhandler(500)
def error500(exception):
    return '捕捉异常，错误信息为：%s' % exception


@blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # 获取页面传递的参数
        username = request.form.get('username')
        password = request.form.get('password')
        # 验证用户名和密码是否正确
        if username == 'clm' and password == '123456':
            # 验证通过, 向session中存入登录成功的标识符
            session['login_status'] = 1
            return redirect(url_for('app.get_response'))
        else:
            return render_template('login.html')