from functools import wraps

import redis
from flask import session, redirect, url_for


# 是否登录验证
from flask_session import Session

from app.models import db
from utils.settings import MYSQL_DATABASES, REDIS_DATABASE


def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        try:
            user_id = session['user_id']
        except:
            return redirect(url_for('user.login_get'))
        return func(*args, **kwargs)
    return check


# 绑定app和db与session
def init_ext(app):
    se = Session()
    se.init_app(app)

    db.init_app(app)


def get_mysqldb_url():
    DRIVER = MYSQL_DATABASES['DRIVER']
    DH = MYSQL_DATABASES['DH']
    ROOT = MYSQL_DATABASES['ROOT']
    PASSWORD = MYSQL_DATABASES['PASSWORD']
    HOST = MYSQL_DATABASES['HOST']
    PORT = MYSQL_DATABASES['PORT']
    NAME = MYSQL_DATABASES['NAME']
    return '{}+{}://{}:{}@{}:{}/{}'.format(DRIVER, DH, ROOT, PASSWORD, HOST, PORT, NAME)


def get_redisdb_url():
    host = REDIS_DATABASE['HOST']
    port = REDIS_DATABASE['PORT']
    return redis.Redis(host=host, port=port)
