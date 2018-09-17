from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from app.models import UserTicket


class UserMiddleware(MiddlewareMixin):

    # 重构拦截请求的方法
    def process_request(self, request):

        # 排除不需要登录验证的地址
        not_login_path = ['/app/login/', '/app/register/']
        path = request.path
        # 校验不需要登录验证的地址
        for n_path in not_login_path:
            # 如果当前访问的地址为登录地址或者注册地址，则直接访问对应视图
            if path == n_path:
                return None

        ticket = request.COOKIES.get('ticket')
        # 如果请求的cookies中没有ticket,则跳转到登录
        if not ticket:
            return HttpResponseRedirect(reverse('app:login'))
        # 通过ticket参数获取当前登录系统的用户信息
        user_ticket = UserTicket.objects.filter(ticket=ticket).first()
        if not user_ticket:
            return HttpResponseRedirect(reverse('app:login'))
        # 设置全局的user
        request.user = user_ticket.user
        # 中间件执行结束，可返回None或者不写
        return None