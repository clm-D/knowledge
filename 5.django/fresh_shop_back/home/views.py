from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from home.forms import UserLoginForm


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 1.表单验证
        form = UserLoginForm(request.POST)
        # 使用is_valid()进行表单验证
        # 2.auth模块验证
        # 3.auth.login登录
        if form.is_valid():
            # form表单验证成功
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                # 如果通过auth拿到对象，就进行登录
                # request.user默认AnonyMouseUser改为user
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home:index'))
            else:
                # auth验证失败，返回信息到页面
                msg = '用户不存在或密码不正确'
                return render(request, 'login.html', {'msg': msg})
        else:
            return render(request, 'login.html', {'form': form})


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect(reverse('home:login'))




def order_list(request):
    if request.method == 'GET':
        return render(request, 'order_list.html')


def user_list(request):
    if request.method == 'GET':
        return render(request, 'user_list.html')