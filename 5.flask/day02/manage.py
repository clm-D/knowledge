import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from app.views import blue
from app.models import db

app = Flask(__name__)

app.register_blueprint(blueprint=blue, url_prefix='/app')

# session配置
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

# 数据库的配置, dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/flask5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 获取session对象，并初始化app
se = Session()
se.init_app(app)

# 绑定app和db
db.init_app(app)

manager = Manager(app=app)


if __name__ == '__main__':
    manager.run()

