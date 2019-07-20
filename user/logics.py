import os
import time
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache

from common import cache_keys, errors, config
from common.hash import my_md5
from common.utils import gen_random_code
from libs import sms, qiniuyun
from libs.http import render_json
from worker import celery_app


def send_verify_code(phone_num):
    """
    发送验证码逻辑
    :param phone_num: 手机号
    :return:
    """
    # 生成验证码
    code = gen_random_code(length=4)

    # 发送验证码
    ret = sms.send_verify_code(phone_num, code)
    if ret:
        cache.set(cache_keys.VERIFY_CODE_KEY_PREFIX.format(phone_num), code, 60*3)
    return ret


def upload_avatar(avatar_name, avatar):
    """
    用户上传文件保存至本地服务器
    :param avatar_name:
    :param avatar:
    :return:
    """
    avatar_path = os.path.join(settings.MEDIA_DIR, avatar_name)+'.png'
    with open(avatar_path, 'wb+') as f:
        for chunk in avatar.chunks():
            f.write(chunk)

    return avatar_path


def upload_qiniuyun(avatar_name, avatar_path):
    """
    本地文件上传到七牛云
    :param avatar_name:
    :param avatar_path:
    :return:
    """
    ret, info = qiniuyun.upload_qiniuyun(avatar_name, avatar_path)
    print("ret:", ret)
    print("info:", info)

    return True if info.status_code ==200 else False


@celery_app.task
def async_upload_avatar(user, avatar):
    avatar_name = 'avatar-{}'.format(my_md5(str(time.time())))

    upload_avatar_path = upload_avatar(avatar_name, avatar)

    ret = upload_qiniuyun(avatar_name, upload_avatar_path)

    if ret:
        user.avatar = urljoin(config.QN_HOST, avatar_name)
        user.save()
