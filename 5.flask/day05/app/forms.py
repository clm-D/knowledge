
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.modles import User


class UserRegisterForm(FlaskForm):
    # 定义用户名和密码都是必填项
    username = StringField('账号', validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])
    password2 = StringField('确认密码', validators=[DataRequired(), EqualTo('password', '两次密码不一致')])

    submit = SubmitField('注册')

    def validators_username(self, field):
        # 验证用户名是否重复
        if User.query.filter(User.username == field.data).first():
            raise ValidationError('账号已存在')

        # 验证用户名长度不能少于4个字符
        if len(field.data) < 4:
            raise ValidationError('注册用户名长度不能少于4个字符')


class UserLoginForm(FlaskForm):
    # 定义用户名和密码都是必填项
    username = StringField('账号', validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])

    submit = SubmitField('登录')

    def validators_username(self, field):

        # 验证用户名长度不能少于4个字符
        if len(field.data) < 4:
            raise ValidationError('用户名长度不能少于4个字符')
