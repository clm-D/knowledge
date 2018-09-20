
from rest_framework import serializers

from app.models import Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定序列化的模型
        model = Student
        # 指定序列化哪些字段

        fields = ['id', 's_name', 's_age']
