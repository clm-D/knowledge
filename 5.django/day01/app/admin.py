from django.contrib import admin

# Register your models here.
from app.models import Student


class StudentAdmin(admin.ModelAdmin):
    # 修改管理后台展示列表的字段
    list_display = ['id', 's_name', 's_age']

    # 按照年龄过滤
    list_filter = ['s_age']

    # 搜索
    search_fields = ['s_name']

    # 分页
    list_per_page = 2

admin.site.register(Student, StudentAdmin)