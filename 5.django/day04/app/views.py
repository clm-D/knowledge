from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from app.models import Student


def index(request):
    if request.method == 'GET':
        stus = Student.objects.all()

        return render(request, 'stus.html', {'students': stus})
        # return render(request, 'index.html', {'students': stus})
        # return HttpResponse('hello')


def del_stu(request, s_id):
    if request.method == 'GET':
        # 删除方法
        # 1.获取url中的id值
        # id = request.GET.get('id')
        # 2.获取id对应的学生对象
        stu = Student.objects.get(pk=s_id)
        # 3.对象.delect()
        stu.delete()

        return HttpResponseRedirect(reverse('app:index'))
        # return HttpResponseRedirect('/app/stu/')


def sel_stu(request, s_id):
    if request.method == 'GET':
        stu = Student.objects.filter(id=s_id).first()
        return render(request, 'stus_sel.html', {'student': stu})
