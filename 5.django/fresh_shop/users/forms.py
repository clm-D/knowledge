from django import forms

from users.models import User


class RegisterForm(forms.Form):
    user_name = forms.CharField(required=True, error_messages={'required': '用户名必填'})
    pwd = forms.CharField(required=True, error_messages={'required': '密码必填'})
    cpwd = forms.CharField(required=True, error_messages={'required': '确认密码必填'})
    email = forms.CharField(required=True, error_messages={'required': '邮箱必填'})
    allow = forms.CharField(required=True, error_messages={'required': '用户条约必须勾选'})

    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('user_name'))
        if user:
            raise forms.ValidationError({'user_name': '该用户名已被注册'})
        if self.cleaned_data.get('pwd') != self.cleaned_data.get('cpwd'):
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
        return self.cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(required=True, error_messages={'required': '用户名必填'})
    password = forms.CharField(required=True, error_messages={'required': '密码必填'})
