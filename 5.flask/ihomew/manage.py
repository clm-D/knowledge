
from flask_script import Manager

from utils.app import create_app

# 创建app
app = create_app()

# 使用Manager管理app
manage = Manager(app)

if __name__ == '__main__':
    # 启动run()
    manage.run()
