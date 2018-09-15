"""
导入规则：
1.先引入python的自带的库

2.再引入第三方

3.最后引入自定义的
"""


from django import forms
from django.contrib.auth.models import User


class UserForm(forms.Form):
    """
    校验注册信息
    """
    username = forms.CharField(required=True, max_length=5, min_length=2, error_messages={'required': '用户名必填', 'max_length': '用户名不能超过5个字符', 'min_length': '用户名不能低于2个字符'})
    password = forms.CharField(required=True, min_length=4, error_messages={'required': '密码必填', 'min_length': '密码不能少于4位'})
    password2 = forms.CharField(required=True, min_length=4, error_messages={'required': '确认密码必填', 'min_length': '确认密码不能少于4位'})

    def clean(self):
        # 校验用户名是否已经注册过
        user = User.objects.filter(username=self.cleaned_data.get('username'))
        if user:
            # 如果已经注册过
            raise forms.ValidationError({'username': '用户名已存在，请重新输入'})
            pass

        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError({'password': '两次密码不一致'})
            pass
        # 教育密码和确认密码是否相同
        return self.cleaned_data


class LoginForm(forms.Form):
    """
    校验登录信息
    """
    username = forms.CharField(required=True, max_length=5, min_length=2, error_messages={'required': '用户名必填', 'max_length': '用户名不能超过5个字符', 'min_length': '用户名不能低于2个字符'})
    password = forms.CharField(required=True, min_length=4, error_messages={'required': '密码必填', 'min_length': '密码不能少于4位'})

    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('username'))
        # 校验用户是否存在
        if not user and self.cleaned_data.get('username'):
            raise forms.ValidationError({'username': '用户名不存在，请先注册再登录'})
        # else:
        #     # 校验密码是否正确
        #     if user.password != self.cleaned_data.get('password'):
        #         raise forms.ValidationError({'password': '用户密码不正确，请重新输入'})

        return self.cleaned_data

