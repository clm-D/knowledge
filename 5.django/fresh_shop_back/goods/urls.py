
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from rest_framework.routers import SimpleRouter

from goods import views

# 引入路由
router = SimpleRouter()
# 使用router注册的地址
router.register(r'^shop', views.ShopView)

urlpatterns = [
    # 商品分类编辑页面
    url(r'^goods_category_detail/(\d+)/', login_required(views.goods_category_detail), name='goods_category_detail'),
    # 商品分类列表
    url(r'^goods_category_list/', login_required(views.goods_category_list), name='goods_category_list'),
    # 商品描述编辑
    url(r'^goods_desc/(\d+)/', login_required(views.goods_desc), name='goods_desc'),
    #添加商品
    url(r'^goods_detail/', login_required(views.goods_detail), name='goods_detail'),
    # 商品列表
    url(r'^goods_list/', login_required(views.goods_list), name='goods_list'),
    # 删除商品
    url(r'^goods_delete/(\d+)/', login_required(views.goods_delete), name='goods_delete'),
    # 商品编辑
    url(r'^goods_edit/(\d+)/', login_required(views.goods_edit), name='goods_edit')
]
urlpatterns += router.urls