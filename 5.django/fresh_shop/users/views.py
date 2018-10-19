from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from cart.models import ShoppingCart
from goods.models import Goods
from orders.models import OrderInfo, OrderGoods
from users.forms import LoginForm, RegisterForm
from users.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 获取页面信息
        # username = request.POST.get('user_name')
        # password = request.POST.get('pwd')
        # email = request.POST.get('email')
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 存储到数据库中
            username = request.POST.get('user_name')
            password = make_password(request.POST.get('pwd'))
            email = request.POST.get('email')
            User.objects.create(username=username, password=password, email=email)
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 验证用户是否存在
            user = User.objects.filter(username=form.cleaned_data['username']).first()
            if user:
                if check_password(form.cleaned_data['password'], user.password):
                    request.session['user_id'] = user.id
                    # 将session中的数据存入用户的购物车中
                    # if request.session.get('goods'):
                    #     session_goods = request.session['goods']
                        # for goods in session_goods:
                        #     goods_id = goods[0]
                        #     num = goods[1]
                        #     is_select = goods[2]
                        #     ShoppingCart.objects.create(user_id=user.id, nums=num, goods_id=goods_id, is_select=is_select)

                    return HttpResponseRedirect(reverse('home:index'))
                else:
                    msg = '密码不正确，请重新输入'
                    return render(request, 'login.html', {'msg': msg})
            else:
                msg = '用户名不存在，请先注册后再登录'
                return render(request, 'login.html', {'msg': msg})
        else:
            # 验证用户名和密码不能为空
            return render(request, 'login.html', {'form': form})



def login_change(request):
    """
    返回给页面用户登录的信息
    """
    user_id = request.session.get('user_id')
    if user_id:
        user = request.user
        info = {}
        info['username'] = user.username
        return JsonResponse({'code': 200, 'info': info})



def logout(request):
    if request.method == 'GET':
        session_key = request.session.session_key
        request.session.delete(session_key)
        return HttpResponseRedirect(reverse('users:login'))


def user_center_info(request):
    if request.method == 'GET':
        info = []
        user = request.user
        info.append(user.username)
        useraddr = UserAddress.objects.filter(user=user).first()
        if useraddr:
            info.append(useraddr.signer_mobile)
            info.append(useraddr.address)
            return render(request, 'user_center_info.html', {'info': info})
        else:
            return render(request, 'user_center_info.html', {'info': info})


def user_center_order(request):
    if request.method == 'GET':
        user = request.user
        order_info = []
        orderinfos = OrderInfo.objects.filter(user=user)
        for orderinfo in orderinfos:
            data = []
            data.append(orderinfo.pay_time)
            data.append(orderinfo.order_sn)
            data.append(orderinfo.pay_status)
            ordergoods = OrderGoods.objects.filter(order_id=orderinfo.id)
            for ordergood in ordergoods:
                goods_info = []
                goods_info.append(Goods.objects.get(pk=ordergood.goods_id))
                goods_info.append(ordergood.goods_nums)
                goods_info.append((ordergood.goods_nums * Goods.objects.get(pk=ordergood.goods_id).shop_price))
                data.append(goods_info)
        order_info.append(data)
        return render(request, 'user_center_order.html', {'order_info': order_info})


def user_center_site(request):
    if request.method == 'GET':
        return render(request, 'user_center_site.html')
