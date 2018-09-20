
from django.conf.urls import url

from rest_framework.routers import SimpleRouter

from app import views

# 引入路由
router = SimpleRouter()
# 使用router注册的地址
router.register(r'^student', views.StudentView)

urlpatterns = [

]
urlpatterns += router.urls
