from django.core.paginator import Paginator
from django.shortcuts import render

from fresh_shop.settings import PAGE_NUMBER
from goods.models import Goods, GoodsCategory


def goods_detail(request, id):
    if request.method == 'GET':
        # 获取某个商品对象
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html', {'goods': goods})


def goods_list(request, id):
    if request.method == 'GET':
        # 获取某类商品对象
        goods = Goods.objects.filter(category=id)
        try:
            page_number = int(request.GET.get('page', 1))
        except:
            page_number = 1
        # 返回类型
        category_types = GoodsCategory.CATEGORY_TYPE
        paginator = Paginator(goods, PAGE_NUMBER)
        page = paginator.page(page_number)
        return render(request, 'list.html', {'page': page, 'id': id})