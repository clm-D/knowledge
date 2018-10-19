
from flask import Flask
from flask_script import Manager
from flask_debugtoolbar import DebugToolbarExtension


from user.models import db
from user.views import user_blueprint

# 创建app
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')


# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/flask5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

# 开启debug模式
app.debug = True

# 初始化app和db
db.init_app(app)

# 初始化debugtoolbar和app
toolbar = DebugToolbarExtension(app=app)

# 使用manage去管理运行的IP、port和debug
manage = Manager(app=app)


if __name__ == '__main__':
    # 运行启动
    manage.run()