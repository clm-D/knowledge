
from flask import Flask
from flask_script import Manager

from app.views import blue, login_manager
from app.modles import db

app = Flask(__name__)

app.register_blueprint(blueprint=blue, url_prefix='/app')

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/f_login_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'secret_key'

# 没有登录跳转地址
login_manager.login_view = 'app.login'

# 绑定
db.init_app(app)

login_manager.init_app(app)

manage = Manager(app)

if __name__ == '__main__':
    manage.run()