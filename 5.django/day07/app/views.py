from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from app.forms import UserForm
from app.models import Users, UserTicket
from utils.functions import get_ticket, is_login


def register(request):
    if request.method == 'GET':
        # 如果请求为get，返回注册页面
        return render(request, 'register.html')

    if request.method == 'POST':
        # 校验参数
        form = UserForm(request.POST)
        # 判断校验是否成功
        if form.is_valid():
            # 注册,使用make_password进行密码加密，否则为明文
            password = make_password(form.cleaned_data['password'])
            Users.objects.create(username=form.cleaned_data['username'], password=password)

            # 跳转到登录界面
            return HttpResponseRedirect(reverse('app:login'))
        else:
            return render(request, 'register.html', {'form', form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 校验登录页面传递的参数
        form = UserForm(request.POST)
        # 使用is_valid()判断是否校验成功
        if form.is_valid():
            # 登录设置
            # 1.通过用户名和密码获取当前的user对象===》》auth.authenticate()

            user = Users.objects.filter(username=form.cleaned_data['username']).first()
            if user:
                # 可以通过username获取到对象
                # 将 user.password和form.cleaned_data['password']进行校验
                if check_password(form.cleaned_data['password'], user.password):
                    # 校验用户名和密码都成功
                    # 1.向cookies中设置随机参数ticket
                    res = HttpResponseRedirect(reverse('app:index'))
                    # set_cookie(key, value, max_age='', expires='')
                    ticket = get_ticket()
                    res.set_cookie('ticket', ticket, max_age=1000)
                    # 2.向表user_ticket中存这个ticket和user的对应关系
                    UserTicket.objects.create(user=user, ticket=ticket)
                    return res
                else:
                    return render(request, 'login.html', {'error': '密码不正确'})

            else:
                # 登录系统的用户名不存在
                return render(request, 'login.html', {'error': '用户名不存在'})

            # 2.设置cookies中的随机值===>>>auth.login()
            # 3.设置user_ticket中的随机值
        else:
            return render(request, 'login.html', {'form', form})


# @is_login
def index(request):
    if request.method == 'GET':
        # # 从cookies中拿ticket
        # ticket = request.COOKIES.get('ticket')
        # # 通过icket去user_ticket表中取数据
        # user_ticket = UserTicket.objects.filter(ticket=ticket).first()
        # if user_ticket:
        #     # 获取当前登录系统的用户
        #     user = user_ticket.user
        #     return render(request, 'index.html', {'user': user})
        # else:
        #     return HttpResponseRedirect(reverse('app:login'))
        return render(request, 'index.html')