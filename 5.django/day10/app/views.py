
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

    # def perform_destroy(self, instance):
    #     instance.first().update(is_delete=1)

