from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from app import views

urlpatterns = [
    # url(r'^'),
    # 注册
    url(r'^register/', views.register, name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 主页面,login_required来添加登录才能进入
    url(r'^index/', login_required(views.index), name='index'),

    # 注销
    url(r'^logout/', login_required(views.logout), name='logout'),

]