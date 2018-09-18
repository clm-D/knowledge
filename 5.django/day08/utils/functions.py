
from django.http import HttpResponseRedirect
from django.urls import reverse


def is_login(func):

    def check(request):
        try:
            # 获取session中已保存的user_id值
            request.session['user_id']
        except:
            # 跳转到登录
            return HttpResponseRedirect(reverse('app:login'))
        return func(request)
    return check