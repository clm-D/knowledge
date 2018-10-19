
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from home import views

urlpatterns = [
    # 登录页面
    url(r'^login/', views.login, name='login'),
    # 安全退出
    url(r'^logout/', login_required(views.logout), name='logout'),
    # 首页
    url(r'^index/', login_required(views.index), name='index'),

    url(r'^order_list/', login_required(views.order_list), name='order_list'),

    url(r'^user_list/', login_required(views.user_list), name='user_list'),
]
