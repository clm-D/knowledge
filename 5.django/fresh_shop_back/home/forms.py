
from django import forms

class UserLoginForm(forms.Form):

    username = forms.CharField(required=True, error_messages={'required': '账号不能为空'})

    password = forms.CharField(required=True, error_messages={'required': '密码不能为空'})

