
from flask import Flask
from flask_script import Manager

from home.views import home_buleprint
from home.user_views import user_blueprint
from home.models import db

app = Flask(__name__)

app.register_blueprint(blueprint=home_buleprint, url_prefix='/home')
app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/ihome_area5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db.init_app(app)

manage = Manager(app)

if __name__ == '__main__':
    manage.run()