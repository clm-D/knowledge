# import logging

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission, Group
from django.http import HttpResponse
from django.shortcuts import render

from app.models import MyUser

# logger = logging.getLogger('console')


def create_user(request):
    if request.method == 'GET':
        MyUser.objects.create_user(username='admin', password='1234')

        return HttpResponse('创建用户成功')


def add_user_permission(request):
    if request.method == 'GET':
        # 给姓名叫admin的用户添加修改用户名的权限
        # 获取到叫admin的用户
        user = MyUser.objects.filter(username='admin').first()
        # 获取到修改用户名的权限
        per = Permission.objects.filter(codename='change_myuser_username').first()
        # 添加权限
        # user.user_permissions.add(per)

        # 删除权限
        # user.user_permissions.remove(per)

        # 清空权限
        user.user_permissions.clear

        return HttpResponse('添加用户权限成功')


def add_group_permission(request):
    if request.method == 'GET':
        # 创建审核组，并分配编辑权限
        group = Group.objects.filter(name='审核组').first()
        if group:
            per_list = ['change_myuser', 'delete_myuser', 'change_myuser_username', 'change_myuser_password']
            # 获取编辑的四个权限
            perms = Permission.objects.filter(codename__in=per_list)
            for per in perms:
                # 添加组和权限之间的关系
                group.permissions.add(per)
                # 删除组和权限之间的关系
                # group.permissions.remove(per)
            return HttpResponse('添加组和权限的关系')
        else:
            # 不存在就创建组
            Group.objects.create(name='审核组')
            return HttpResponse('审核组没有创建，请先创建')


def add_user_group(request):
    if request.method == 'GET':
        # 给admin用户分配审核组
        # 先获取到对应的用户和组
        user = MyUser.objects.filter(username='admin').first()
        group = Group.objects.filter(name='审核组').first()

        # 给admin用户分配审核组
        user.groups.add(group)

        return HttpResponse('分配组成功')

# 查询用户的权限
def user_permission(request):
    if request.method == 'GET':
        user = MyUser.objects.filter(username='admin').first()
        # 查询user的权限

        # 1.通过权限直接查询
        per = user.user_permissions.all().values('codename')

        # 2.通过组来查询
        # 方法1：
        perms = user.groups.first().permissions.all().values('codename')

        # 方法2：得到权限集合
        user.get_group_permissions()

        # 获取用户所有的权限
        user.get_all_permissions()

        return HttpResponse(' ')


@permission_required('app.change_myuser_username')
def index(request):
    if request.method == 'GET':
        # logging.info('index方法')
        # change_myuser_username
        user = request.user
        # return HttpResponse('我是首页，我需要有修改用户名的权限才能访问')
        return render(request, 'index.html')