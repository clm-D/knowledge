
from django.conf.urls import url

from users import views

urlpatterns = [
    # 注册
    url(r'^register/', views.register, name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),

    # 登录后修改信息
    url(r'^login_change/', views.login_change, name='login_change'),
    # 注销
    url(r'^logout/', views.logout, name='logout'),

    url(r'^user_center_info/', views.user_center_info, name='user_center_info'),

    url(r'^user_center_order/', views.user_center_order, name='user_center_order'),

    url(r'^user_center_site/', views.user_center_site, name='user_center_site'),
]