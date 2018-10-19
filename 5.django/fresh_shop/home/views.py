from django.shortcuts import render

from goods.models import Goods, GoodsCategory


def index(request):
    if request.method == 'GET':
        """
        想要的数据样式
        {'goods_1': [goods objects, goods objects, goods objects, goods objects], 
        'goods_2': [],……}
        """
        # 获取所有商品的分类
        category_types = GoodsCategory.CATEGORY_TYPE
        # 获取商品，按照id降序排序
        goods = Goods.objects.all().order_by('-id')
        # 循环商品分析，并组装结果
        data_all = {}
        for type in category_types:
            data = []
            count = 0
            for good in goods:
                # data中只存4条数据
                if ((count < 4) and (type[0] == good.category.category_type)):
                    data.append(good)
                    count += 1
            data_all['goods_'+str(type[0])] = data

        return render(request, 'index.html', {'data_all': data_all, 'category_types': category_types})









