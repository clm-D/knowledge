import os
import random
import re

from flask import Blueprint, render_template, request,\
    session, jsonify, redirect, url_for

from app.models import db, User
from utils import status_code
from utils.functions import is_login
from utils.settings import UPLOAD_DIR

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'


@user_blueprint.route('/register/', methods=['GET'])
def register_get():
    return render_template('register.html')


@user_blueprint.route('/login/', methods=['GET'])
def login_get():
    return render_template('login.html')


@user_blueprint.route('/get_code/')
def get_code():
    # 获取随机长度为4的验证码
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    code = ''
    for i in range(4):
        code += random.choice(s)
    # 将状态码code存放在session中
    session['code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blueprint.route('/register/', methods=['POST'])
def register_post():
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if not all([mobile, imagecode, password, password2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_VALID)
    if session.get('code') != imagecode:
        return jsonify(status_code.USER_REGISTER_CODE_ERROR)
    if not re.match(r'^1[3456789]\d{9}', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_INVALID)
    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_ERROR)
    user = User.query.filter(User.phone == mobile).all()
    if user:
        return jsonify(status_code.USER_REGISTER_MOBILE_EXSIST)
    else:
        user = User()
        user.phone = mobile
        user.password = password
        user.name = mobile
        try:
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except:
            return jsonify(status_code.DATABASE_ERROR)


@user_blueprint.route('/login/', methods=['POST'])
def login_post():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    if not all([mobile, password]):
        return jsonify(status_code.USER_LOGIN_PARAMS_VALID)
    user = User.query.filter(User.phone == mobile).first()
    if user:
        if user.check_pwd(password):
            session['user_id'] = user.id
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_INVALID)
    else:
        return jsonify(status_code.USER_LOGIN_PHONE_INVALID)


@user_blueprint.route('/logout/', methods=['GET'])
@is_login
def logout():
    session.clear()
    return jsonify(status_code.SUCCESS)


@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


@user_blueprint.route('/user_info/', methods=['GET'])
@is_login
def user_info():
    user_id = session['user_id']
    user = User.query.get(user_id)
    user_info = user.to_basic_dict()
    return jsonify(user_info=user_info, code=status_code.OK)


@user_blueprint.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


@user_blueprint.route('/profile_get/', methods=['GET'])
@is_login
def profile_get():
    user = User.query.get(session['user_id'])
    if user.name or user.avatar:
        return jsonify({'code': 200, 'username': user.name, 'user_avatar': user.avatar})
    else:
        return jsonify(status_code.OK)


@user_blueprint.route('/profile/', methods=['PATCH'])
@is_login
def profile_patch():
    avatar = request.files.get('avatar')
    name = request.form.get('name')
    if avatar:
        if not re.match(r'image/*', avatar.mimetype):
            return jsonify(status_code.USER_USERINFO_PROFILE_ACATAR_INVALID)
        file_path = os.path.join(UPLOAD_DIR, avatar.filename)
        avatar.save(file_path)
        # 保存到数据库
        user = User.query.get(session['user_id'])
        avatar_addr = os.path.join('upload', avatar.filename)
        user.avatar = avatar_addr
        user.add_update()
        return jsonify({'code': status_code.OK, 'avatar': avatar_addr})
    if name:
        if User.query.filter(User.name == name).count():
            return jsonify(status_code.USER_USERINFO_NAME_EXSITS)
        user = User.query.get(session['user_id'])
        user.name = name
        user.add_update()
        return jsonify({'code': status_code.OK, 'name': name})
    return render_template('profile.html')


@user_blueprint.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


@user_blueprint.route('/auth_get/', methods=['GET'])
def auth_get():
    user = User.query.get(session['user_id'])
    user = user.to_auth_dict()
    return jsonify({'code': status_code.OK, 'user': user})


@user_blueprint.route('/auth_post/', methods=['POST'])
def auth_post():
    read_name = request.form.get('read_name')
    id_card = request.form.get('id_card')

    if not all([read_name, id_card]):
        return jsonify(status_code.USER_USERINFO_ID_NAME_CARD_INVALID)
    if not re.match(r'[1-9]\d{16}[0-9X]', id_card):
        return jsonify(status_code.USER_USERINFO_ID_CARD_INVALID)
    user = User.query.get(session['user_id'])
    user.id_name = read_name
    user.id_card = id_card
    user.add_update()
    return jsonify(status_code.OK)