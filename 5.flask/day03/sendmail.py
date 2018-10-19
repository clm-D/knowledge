from threading import Thread

from flask import Flask
from flask_mail import Mail,Message


app = Flask(__name__)

# 邮箱配置
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '15775977568@163.com'
app.config['MAIL_PASSWORD'] = 'clm1677'

mail = Mail(app=app)


@app.route('/send_mail')
def send_mail():
    # 发送邮件
    message = Message('买股票吗？', sender=app.config['MAIL_USERNAME'], recipients=['1677010203@qq.com'])
    message.body = '678342号，买进，必涨,爱信不信'

    send_email(message)

    return '发送成功'


def send_email(msg):
    with app.app_context():
        mail.send(msg)


if __name__ == '__main__':
    app.run(port=8080)
