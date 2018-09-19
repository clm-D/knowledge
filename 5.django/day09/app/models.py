from django.db import models

from django.contrib.auth.models import User, Group, Permission, AbstractUser


class MyUser(AbstractUser):
    """
    自定义django自带的User模型
    """
    is_delete = models.BooleanField(default=0, verbose_name='是否删除')

    class Meta:
        # ('权限名', '描述')
        permissions = (
            ('change_myuser_username', '修改用户名'),
            ('change_myuser_password', '修改密码'),
        )
