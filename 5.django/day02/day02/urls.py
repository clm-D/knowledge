"""day02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('create_stu/', views.create_stu),
    url('select_stu/', views.select_stu),
    url('delete_stu/', views.delete_stu),
    url('update_stu/', views.update_stu),

    url('create_stu_info/', views.create_stu_info),
    url('stu_add_stuinfo/', views.stu_add_stuinfo),
    url('sel_phone_by_stu/', views.sel_phone_by_stu),
    url('sel_stu_by_phone/', views.sel_stu_by_phone),

    url('create_grade/', views.create_grade),
    # url('create_grade_stu/', views.create_grade_stu),
    url('sel_grade_by_stu/', views.sel_grade_by_stu),

    url('create_course/', views.create_course),
    url('create_stu_course/', views.create_stu_course),
]
