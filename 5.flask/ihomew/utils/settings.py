import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# static路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# templates路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# 上传路径
UPLOAD_DIR = os.path.join(os.path.join(STATIC_DIR, 'media'), 'upload')

# 数据库配置
MYSQL_DATABASES = {
    'DRIVER': 'mysql',
    'DH': 'pymysql',
    'ROOT': 'root',
    'PASSWORD': '1234',
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'NAME': 'ihome_area'
}

REDIS_DATABASE = {
    'HOST': '127.0.0.1',
    'PORT': 6379
}