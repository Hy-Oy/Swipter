from common.utils import gen_random_code
from libs import sms


def send_verify_code(phone_num):
    """
    发送验证码逻辑
    :param phone_num: 手机号
    :return:
    """
    # 生成验证码
    code = gen_random_code(length=4)

    # 发送验证码
    return sms.send_verify_code(phone_num, code)