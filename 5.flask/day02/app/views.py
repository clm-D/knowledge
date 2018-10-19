
from flask import Blueprint, redirect, url_for,\
    request, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db, User
from utils.functions import is_login

blue = Blueprint('app', __name__)


@blue.route('/index/', methods=['GET'])
@is_login
def index():
    return render_template('index.html')


@blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 校验用户名和密码不能为空
        if not all([username, password]):
            msg = '用户名或密码不能为空'
            return render_template('login.html', msg=msg)
        # 获取用户
        user = User.query.filter(User.username==username).first()
        # 判断用户是否存在
        if user:
            # 判断密码是否正确
            if check_password_hash(user.password, password):
                session['login_status'] = 1
                return redirect(url_for('app.index'))
            else:
                msg = '密码不正确'
                return render_template('login.html', msg=msg)
        else:
            msg = '用户名不存在'
            return render_template('login.html', msg=msg)


@blue.route('/scores/', methods=['GET'])
def scores():

    # render(request, 'xxx.html', {k1:v1, k2:v2})
    stu_scores = [80, 66, 73, 2]
    content_h2 = '<h2>hello python</h2>'
    return render_template('scores.html',
                           stu_scores=stu_scores,
                           content_h2=content_h2)


@blue.route('/create_db/', methods=['GET'])
def create_db():
    db.create_all()
    return '创建表成功'


@blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            msg = '用户名或密码不能为空'
            return render_template('register.html', msg=msg)
        # 保存注册信息
        user = User()
        user.username = username
        # 密码加密
        user.password = generate_password_hash(password)
        # 保存
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('app.login'))