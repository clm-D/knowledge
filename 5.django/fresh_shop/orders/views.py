from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from goods.models import Goods
from orders.models import OrderGoods, OrderInfo
from utils.functions import get_order_sn



def place_order(request):
    if request.method == 'GET':
        # 登录系统用户, 获取购物车的商品信息
        user_id = request.session.get('user_id')
        # 获取当前勾选的商品用于下单
        shop_cart = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        data = [(Goods.objects.get(pk=cart.goods_id), cart.nums, (Goods.objects.get(pk=cart.goods_id).shop_price * cart.nums)) for cart in shop_cart]
        count = len(data)
        all_price = 0
        for goods in data:
            all_price += goods[2]
        return render(request, 'place_order.html', {'data': data, 'count': count, 'all_price': all_price})

    if request.method == 'POST':
        """
        接收ajax请求，创建订单
        """
        # 1. 下单，选择购物车中is_selec为True的商品
        # 2. 创建订单
        # 3. 创建订单和商品之间的关联关系表， order_goods表
        # 4. 删除购物车中已下单的商品
        user_id = request.session.get('user_id')
        # 获取购物车中当前登录用户勾选的商品
        carts = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        # 订单货号
        order_sn = get_order_sn()
        # 订单金额
        order_mount = 0
        # 判断购物车是否有商品，有就创建订单
        if carts:
            for cart in carts:
                order_mount += cart.nums * cart.goods.shop_price
            # 创建订单
            order = OrderInfo.objects.create(user_id=user_id, order_sn=order_sn, order_mount=order_mount)

            for cart in carts:
                # 创建订单与商品之间的详情表
                OrderGoods.objects.create(order_id=order.id, goods_id=cart.goods_id, goods_nums=cart.nums)

            carts.delete()
            # 删除session中的商品信息
            request.session.pop('goods')

            return JsonResponse({'code': 200, 'msg': '请求成功'})
        else:
            return JsonResponse({'code': 202, 'msg': '请求失败'})