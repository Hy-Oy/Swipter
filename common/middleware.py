from django.utils.deprecation import MiddlewareMixin

from common import errors
from common.errors import LogicException, LogicError
from libs.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        """
        自定义中间件
        白名单：request.path
        根据　request.session['uid']判断登录状态
        :return:
        """

        WHITE_LIST =[
            '/api/user/verify-phone',
            '/api/user/login',
        ]

        if request.path in WHITE_LIST:
            return

        uid = request.session.get('uid')

        if not uid:
            return render_json(code=errors.LOGIN_REQUIRED_ERR)

        request.user = User.objects.get(pk=uid)


class LogicExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, (LogicException, LogicError)):
            return render_json(code=exception.code)
