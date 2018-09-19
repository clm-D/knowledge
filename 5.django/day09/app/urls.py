
from django.conf.urls import url

from app import views

urlpatterns = [
    # 创建admin用户
    url(r'^create_user/', views.create_user, name='create_user'),
    # 给用户添加权限
    url(r'^add_user_permission/', views.add_user_permission, name='add_user_permission'),
    # 给组分配权限
    url(r'^add_group_permission/', views.add_group_permission, name='add_group_permission'),
    # 给admin用户分配审核组
    url(r'^add_user_group/', views.add_user_group, name='add_user_group'),
    # 查询某个用户的权限列表
    url(r'^user_permission/', views.user_permission, name='user_permission'),

    # 进入index.html页面
    url(r'^index/', views.index, name='index')
]
