from django.db import models

# Create your models here.


class Student(models.Model):

    # 姓名长度最大10，不能重复
    s_name = models.CharField(max_length=10, unique=True)

    s_age = models.IntegerField(default=16)

    class Meta:
        db_table = 'student'
