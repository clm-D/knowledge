from django.db import models

# Create your models here.
class Student(models.Model):

    s_name = models.CharField(max_length=10, verbose_name='姓名')

    s_age= models.IntegerField()
