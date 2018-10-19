
import os
import re

from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from app.forms import UserRegisterForm, UserLoginForm
from app.modles import db, User
from utils.settings import UPLOAD_DIR

blue = Blueprint('app', __name__)

login_manager = LoginManager()


@blue.route('/register/', methods=['GET', 'POST'])
def register():
    # 表单对象
    form = UserRegisterForm()
    if request.method == 'GET':

        return render_template('register.html', form=form)

    if request.method == 'POST':
        # 验证提交的字段信息
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            # 实现注册，保存用户信息到User模型中
            user = User()
            user.username = username
            user.password = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('app.login'))
        else:
            # 验证失败， form.errors中存在错误信息
            return render_template('register.html', form=form)


@blue.route('/create_db/')
def create_db():
    db.create_all()
    return '数据表创建成功'


# 回调
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@blue.route('/login/', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter(User.username == username).first()
            # 验证用户是否存在
            if user:
                # 验证密码
                if check_password_hash(user.password, password):
                    # 密码正确
                    # 实现登录, django中auth.login(request, user)
                    login_user(user)
                    return redirect(url_for('app.index'))
                else:
                    error = '密码错误'
                    return render_template('login.html', error=error, form=form)
            else:
                # 账号不存在
                error = '账号不存在！'
                return render_template('login.html', error=error, form=form)
        else:
            return render_template('login.html', form=form)


# @blue.before_request
# def bf_request():
#     return 'before_request'


@blue.route('/index/', methods=['GET', 'POST'])
@login_required
@blue.before_request
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # 获取图片
        icons = request.files.get('icons')
        # 保存save(path)到本地/static/media/upload

        # 作业：
        # 1.只保存图片
        # 2.中间件，钩子
        # @blue.before_request
        # @blue.after_request
        # @blue.teardown_request

        str = r'.+\.(jpg|gif|png|bmp)'
        match1 = re.match(str, icons.filename)

        if match1:
            file_path = os.path.join(UPLOAD_DIR, icons.filename)
            icons.save(file_path)
            # 保存到数据库中
            user = current_user
            user.icons = os.path.join('upload', icons.filename)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('app.index'))
        else:
            error = '请上传图片格式的文件'
            return render_template('index.html', error=error)


@blue.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.login'))