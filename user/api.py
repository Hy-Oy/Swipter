from django.core.cache import cache
from django.http import JsonResponse

from common import errors, cache_keys
from common.utils import is_phonenum
from libs.http import render_json
from user import logics
from user.models import User


def verify_phone(request):
    """
           1、验证手机格式
           2、生成验证码
           3、保存验证码
           4、发送验证码
    """
    phone_num = request.POST.get('phone_num')

    if is_phonenum(phone_num):
        """
            生成验证码
            发送验证码
        """
        if logics.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SMS_SEND_ERR)
    else:
        return render_json(code=errors.PHONE_NUM_ERR)


def login(request):
    """
    登录或注册接口
    如果手机号存在则登录，不存在则注册
    # １、检测验证码是否正确
    # ２、注册或登录
    :param request:
    :return:
    """
    phone_num = request.POST.get('phone_num','')
    code = request.POST.get('code','')
    cache_code = cache.get(cache_keys.VERIFY_CODE_KEY_PREFIX.format(phone_num))
    if cache_code != code:
        return render_json(code=errors.VERIFY_CODE_ERR)
    user, created = User.objects.get_or_create(phonenum=phone_num)

    #设置登录状态
    request.session['uid'] = user.id

    return render_json(data=user.to_dic)