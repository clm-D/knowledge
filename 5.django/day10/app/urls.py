
from django.conf.urls import url

from rest_framework.routers import SimpleRouter

from app import views

# 引入路由
router = SimpleRouter()
# 使用router注册的地址
router.register(r'^student', views.StudentView)

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^add/', views.add, name='add'),
    url(r'^delete/', views.add, name='delete'),
    url(r'^update/', views.add, name='update'),
]
urlpatterns += router.urls
