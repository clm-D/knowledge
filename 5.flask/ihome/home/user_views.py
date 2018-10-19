import os
import random
import re

from flask import Blueprint, render_template, request, session, jsonify

from home.models import User
from utils import status_code
from utils.functions import is_login
from utils.settings import UPLOAD_DIR

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blueprint.route('/get_code/', methods=['GET'])
def get_code():
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['code'] = code
    return jsonify({'code': '200', 'msg': '请求成功', 'data': code})


@user_blueprint.route('/register_post/', methods=['POST'])
def register_post():
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if imagecode != session['code']:
        return jsonify(status_code.USER_REGISTER_CODE_ERROR)
    if not all([mobile, imagecode, password, password2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_VALID)
    if re.match(r'1[3456789]/d{9}', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_INVALID)
    if password2 != password:
        return jsonify(status_code.USER_REGISTER_PASSWORD_ERROR)
    user = User.query.filter(User.phone == mobile).all()
    if user:
        return jsonify(status_code.USER_REGISTER_MOBILE_EXSIST)
    user = User()
    user.phone = mobile
    user.password = password
    user.name = mobile
    user.add_update()
    return jsonify({'code': status_code.OK})


@user_blueprint.route('/login_post/', methods=['POST'])
def login_post():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    if not all([mobile, password]):
        return jsonify(status_code.USER_LOGIN_PARAMS_VALID)
    user = User.query.filter(User.phone == mobile).first()
    if not user:
        return jsonify(status_code.USER_LOGIN_PHONE_INVALID)
    if not user.check_pwd(password):
        return jsonify(status_code.USER_LOGIN_PASSWORD_INVALID)
    return jsonify(status_code.SUCCESS)


@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


@user_blueprint.route('/my_get/', methods=['GET'])
@is_login
def my_get():
    user = User.query.get(session['user_id'])
    username = user.name
    mobile = user.phone
    avatar = user.avatar
    return jsonify({'code': '200', 'username': username, 'mobile': mobile, 'avatar': avatar})


@user_blueprint.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


@user_blueprint.route('/profile_get/', methods=['GET'])
@is_login
def profile_get():
    user = User.query.get(session['user_id'])
    icon = user.avatar
    username = user.name
    return jsonify({'code': status_code.OK, 'icon': icon, 'username': username})


@user_blueprint.route('/profile_patch/', methods=['PATCH'])
@is_login
def profile_patch():
    avatar = request.files.get('avatar')
    name = request.form.get('name')
    user = User.query.get(session['user_id'])
    if avatar:
        if not re.match(r'image/*', avatar.mimetype):
            return jsonify(status_code.USER_USERINFO_PROFILE_ACATAR_INVALID)
        file_path = os.path.join(UPLOAD_DIR, avatar.filename)
        avatar.save(file_path)
        # 保存到数据库中
        avatar_url = os.path.join('upload', avatar.filename)
        user.avatar = avatar_url
        user.add_update()
        return jsonify({'code': status_code.OK, 'avatar_url': avatar_url})
    if name:
        if user.name == name:
            return jsonify(status_code.USER_USERINFO_NAME_EXSITS)
        user.name = name
        user.add_update()
        return jsonify({'code': status_code.OK, 'name': name})