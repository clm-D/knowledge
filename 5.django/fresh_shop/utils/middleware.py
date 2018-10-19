import re

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from users.models import User


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 登录验证中间件
        # 不需要登录验证的url地址
        not_need_check = ['/home/index/', '/users/login/', '/users/register/',
                          '/cart/my_cart/', '/cart/f_price/', '/cart/add_cart/',
                          '/goods/goods_list/(\d+)/','/goods/goods_detail/(\d+)/','/media/(.*)', '/static/(.*)']
        path = request.path
        for not_path in not_need_check:
            # 匹配当前url地址是不是不需要登录的验证
            if re.match(not_path, path):
                return None

        # 登录验证开始
        user_id = request.session.get('user_id')
        # 没有登录，获取不到user_id参数，则跳转到登录页面
        if not user_id:
            return HttpResponseRedirect(reverse('users:login'))
        # 给request.user赋值为当前登录系统的用户
        user = User.objects.get(pk=user_id)
        request.user = user

        return None


class UserSessionMiddlewart(MiddlewareMixin):
    # 同步session数据到shopping_cart表中

    def process_request(self, request):
        # 判断用户是否登录
        user_id = request.session.get('user_id')
        if user_id:
            # 同步, 获取到session中的商品数据
            session_goods = request.session.get('goods')
            if session_goods:
                # 1.如果购物车数据库没有session中的数据，则创建
                # 2.如果有，就更新
                # session_goods的结构：[[id, num, is_select],[id, num, is_select], ……]
                for goods in session_goods:
                    # 查询购物车中是否存在商品信息
                    cart = ShoppingCart.objects.filter(goods_id=goods[0], user_id=user_id).first()

                    if cart:
                        # 如果购物车中存在session中保存的商品信息，则修改数据和状态
                        if cart.nums != goods[1]:
                            # 同步商品数量
                            cart.nums = int(goods[1])
                        # 同步商品选择状态
                        cart.is_select = int(goods[2])
                        cart.save()
                    else:
                        ShoppingCart.objects.create(user_id=user_id, goods_id=goods[0], nums=int(goods[1]), is_select=int(goods[2]))
                return None

