import random
import re

pattern = re.compile(r'^1[3-9]\d{9}$')
def is_phonenum(phonenum):
    '''
    验证手机号格式
    :param phonenum:
    :return:
    '''
    return True if pattern.match(phonenum) else False


def gen_random_code(length=4):
    if length < 1 :
        length = 1

    if not isinstance(length,int):
        length = 1

    code = random.randrange(10**(length-1), 10**length)

    return str(code)