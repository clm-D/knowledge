from django.shortcuts import render
from rest_framework import viewsets, mixins

from app.models import Student
from app.serializers import StudentSerializer


class StudentView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    # 返回数据
    queryset = Student.objects.all()
    # 序列化结果
    serializer_class = StudentSerializer

    def perform_destroy(self, instance):
        instance.is_delete=1
        instance.save()


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')


def delete(request):
    if request.method == 'GET':
        return render(request, 'delete.html')


def update(request):
    if request.method == 'GET':
        return render(request, 'update.html')
