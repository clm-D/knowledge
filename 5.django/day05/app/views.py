from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from app.forms import UserForm, LoginForm
from app.models import Student


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        # 校验页面中传递的参数是否天兴完整
        form = UserForm(request.POST)
        # username = request.POST.get('username')
        # is_valid()：判断表单是否验证通过
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')

            User.objects.create_user(username=username, password=password)
            return HttpResponseRedirect(reverse('app:login'))
            # # 验证密码是否一致
            # if password == password2:
            #     # 创建普通用户
            #     User.objects.create_user(username=username, password=password)
            #     return render(request, 'register.html')
            # else:
            #     return render(request, 'register.html')
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 表单验证，用户名和密码是否填写，用户是否存在
        form = LoginForm(request.POST)
        if form.is_valid():
            # 校验用户名和密码，判断返回的对象是否为空，如果不为空，则位user对象
            user = auth.authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user:
                # 用户名和密码正确，则登录
                auth.login(request, user)
                return HttpResponseRedirect(reverse('app:index'))
            else:
                # 密码不正确
                return render(request, 'login.html', {'error': '密码错误'})
        else:
            return render(request, 'login.html', {'form': form})



def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def logout(request):
    if request.method == 'GET':
        # 注销
        auth.logout(request)
        return HttpResponseRedirect(reverse('app:login'))