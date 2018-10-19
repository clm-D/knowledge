from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from goods.models import Goods


def add_cart(request):
    if request.method == 'POST':
        # 添加到购物车
        # 添加到session中的数据格式为：
        # key ===> goods,
        # value ===> [[id1, num1], [id2, num2],……]

        # 1. 没有登录的情况
        # 1.1 添加到购物车的数据，其实就是添加到session中
        # 1.2 如果商品已经添加到session中，就修改商品个数
        # 1.3 如果商品没有添加到session中， 则添加

        # 获取从Ajax中传递的商品的id和商品个数
        goods_id = request.POST.get('goods_id')
        goods_num = int(request.POST.get('goods_num'))
        goods_select = int(request.POST.get('goods_select'))
        # 组装存储的数据结构
        goods_list = [goods_id, goods_num, goods_select]
        # 判断在session中是否存储了商品信息
        if request.session.get('goods'):
            # 标识符：用于判断当前加入到购物车的商品
            # 如果购物车中已经存在该商品，则修改flag为1，否则flag还为0
            flag = 0
            # 说明购物车中已经存储了商品信息
            session_goods = request.session['goods']
            for goods in session_goods:
                # 循环判断，判断加入到session中的商品是否已经存在于session中
                if goods_id == goods[0]:
                    goods[1] = int(goods[1]) + goods_num
                    # 标识符，修改session中的商品后，标识符修改为1
                    flag = 1
            # flag为0，表示添加到session中的商品之前并没有添加
            if not flag:
                session_goods.append(goods_list)
            # 修改成功session中商品的信息
            request.session['goods'] = session_goods
            cart_count = len(session_goods)
        else:
            # 说明购物车中还没有存储商品信息
            data = []
            data.append(goods_list)
            request.session['goods'] = data
            cart_count =1

        return JsonResponse({'code': 200, 'cart_count':cart_count })

#
# def add_cart2(request):
#     if request.method == 'POST':
#         # 添加到购物车
#         # 添加到session中的数据格式为：
#         # key ===> goods,
#         # value ===> [[id1, num1], [id2, num2],……]
#
#         # 1. 没有登录的情况
#         # 1.1 添加到购物车的数据，其实就是添加到session中
#         # 1.2 如果商品已经添加到session中，就修改商品个数
#         # 1.3 如果商品没有添加到session中， 则添加
#
#         # 获取从Ajax中传递的商品的id和商品个数
#         goods_id = request.POST.get('goods_id')
#         goods_num = int(request.POST.get('goods_num'))
#         goods_select = int(request.POST.get('goods_select'))
#         # 组装存储的数据结构
#         goods_list = [goods_id, goods_num, goods_select]
#         # 判断在session中是否存储了商品信息
#         if request.session.get('goods'):
#             # 标识符：用于判断当前加入到购物车的商品
#             # 如果购物车中已经存在该商品，则修改flag为1，否则flag还为0
#             flag = 0
#             # 说明购物车中已经存储了商品信息
#             session_goods = request.session['goods']
#             for goods in session_goods:
#                 # 循环判断，判断加入到session中的商品是否已经存在于session中
#                 if goods_id == goods[0]:
#                     goods[1] = goods_num
#                     # 标识符，修改session中的商品后，标识符修改为1
#                     flag = 1
#             # flag为0，表示添加到session中的商品之前并没有添加
#             if not flag:
#                 session_goods.append(goods_list)
#             # 修改成功session中商品的信息
#             request.session['goods'] = session_goods
#             cart_count = len(session_goods)
#         else:
#             # 说明购物车中还没有存储商品信息
#             data = []
#             data.append(goods_list)
#             request.session['goods'] = data
#             cart_count =1
#
#         return JsonResponse({'code': 200, 'cart_count':cart_count })


def my_cart(request):
    if request.method == 'GET':
        # 需要判断用户是否登录， session.get('user_id')
        # 1. 如果登录，则购物车中展示当前登录用户的购物车表中的数据
        # 2. 如果没有登录，则购物车页面中展示session中的数据
        user_id = request.session.get('user_id')
        if user_id:
            # 登录系统用户, 获取购物车的商品信息
            shop_cart = ShoppingCart.objects.filter(user_id=user_id)
            data = [(Goods.objects.get(pk=cart.goods_id), cart.nums, cart.is_select) for cart in shop_cart]

            return render(request, 'cart.html', {'data': data})
        else:
            # 没有登录
            # 判断在session中是否存储了商品信息
            if request.session.get('goods'):
                session_goods = request.session['goods']
                # 将数据拆分
                data = []
                count = len(session_goods)
                all = 0
                for goods in session_goods:
                    good = Goods.objects.get(pk=goods[0])
                    num = goods[1]
                    is_select = goods[2]
                    total = int(num) * good.shop_price
                    all += total
                    goods_list = [good, num, is_select]
                    data.append(goods_list)
                return render(request, 'cart.html', {'data': data, 'count': count})
            else:
                return render(request, 'cart.html')


def f_price(requset):
    """
    返回购物车或session中商品的的价格和总价
    {key1:[[id1, total_price1],……], key2:all_price}
    """
    user_id = requset.session.get('user_id')
    if user_id:
        # 获取当前登录系统的用户的购物车中的数据
        carts = ShoppingCart.objects.filter(user_id=user_id)
        cart_data = {}
        data_all = []
        all_price = 0
        for cart in carts:
            data = []
            data.append(cart.goods_id)
            data.append(float(cart.nums) * float(cart.goods.shop_price))
            data_all.append(data)
            if cart.is_select:
                all_price += cart.nums * cart.goods.shop_price
        cart_data['goods_price'] = data_all
        cart_data['all_price'] = all_price
        return JsonResponse({'code': 200, 'cart_data': cart_data})
    else:
        # 拿到session中所有的商品信息
        session_goods = requset.session.get('goods')
        cart_data = {}
        data_all = []
        all_price = 0
        for goods in session_goods:
            data = []
            data.append(goods[0])
            good = Goods.objects.get(pk=goods[0])
            data.append(float(goods[1]) * float(good.shop_price))
            data_all.append(data)
            # 判断如果商品勾选了，才计算总价格
            if goods[2]:
                all_price += float(goods[1]) * float(good.shop_price)
        cart_data['goods_price'] = data_all
        cart_data['all_price'] = all_price
        return JsonResponse({'code': 200, 'cart_data': cart_data})
