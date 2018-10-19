
from django.conf.urls import url

from goods import views

urlpatterns = [
    # 商品详情
    url(r'^goods_detail/(\d+)/', views.goods_detail, name='goods_detail'),

    # 商品分类列表
    url(r'^goods_list/(\d+)/', views.goods_list, name='goods_list'),
]