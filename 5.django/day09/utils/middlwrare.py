
from django.utils.deprecation import MiddlewareMixin

from app.models import MyUser


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        user = MyUser.objects.get(username='admin')
        request.user = user

        return None
