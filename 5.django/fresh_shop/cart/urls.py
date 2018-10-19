
from django.conf.urls import url

from cart import views

urlpatterns = [
    # 添加到购物车
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    # 按加减添加到购物车
    # url(r'^add_cart2/', views.add_cart2, name='add_cart2'),
    # 购物车页面
    url(r'^my_cart/', views.my_cart, name='my_cart'),
    # 刷新价格
    url(r'^f_price/', views.f_price, name='f_price'),
]