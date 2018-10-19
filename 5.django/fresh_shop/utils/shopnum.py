from cart.models import ShoppingCart


def shopnums(request):
    user_id = request.session.get('user_id')
    if user_id:
        shop_carts = ShoppingCart.objects.filter(user_id=user_id)
        shop_nums = len(shop_carts)
        return {'shop_nums': shop_nums}
    else:
        goods = request.session.get('goods')
        if goods:
            shop_nums = len(goods)
            return {'shop_nums': shop_nums}
        return {'shop_nums': 0}
