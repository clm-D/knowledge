
import random
import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse

from app.models import UserTicket


# def is_timeout(user_ticket):
#     # 1.获取当前时间
#     now_time1 = datetime.datetime.now()
#     now_time1_c = now_time1.timestamp()


def get_ticket():
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    ticket = ''
    for i in range(25):
        ticket += random.choice(s)
    return ticket


def is_login(func):

    def check(request):
        ticket = request.COOKIES.get('ticket')
        # 如果cookie中存在设置的ticket则通过user_ticket表进行校验
        if ticket:
            # 通过user_ticket表获取对象
            user_ticket = UserTicket.objects.filter(ticket=ticket).first()
            if user_ticket:
                return func(request)
            else:
                # ticket参数错误，则跳转到登录
                return HttpResponseRedirect(reverse('app:login'))
        else:
            # 没有ticket就说明没有登录
            return HttpResponseRedirect(reverse('app:login'))
    return check


def is_logout(func):

     def out(request):
         ticket = request.COOKIES.get('ticket')

         UserTicket.objects.filter(ticket=ticket).first().delete()

         return func(request)

     return out
