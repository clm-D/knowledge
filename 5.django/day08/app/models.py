from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255, verbose_name='密码')
    icon = models.ImageField(upload_to='upload', null=True, verbose_name='头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    operate_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'users'


class UserTicket(models.Model):
    user = models.ForeignKey(Users)
    ticket = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    max_age = models.IntegerField(verbose_name='存活时间')

    class Meta:
        db_table = 'user_ticket'
