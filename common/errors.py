'''
状态码，
业务码
'''
ok = 0

# 系统保留状态码：１０００－１９９９

# 用户系统：２０００－２９９９
PHONE_NUM_ERR = 2001 #手机号码错误
SMS_SEND_ERR = 2002 #发送失败
VERIFY_CODE_ERR = 2003  #验证失败
LOGIN_REQUIRED_ERR = 2004  #未登录
AVATAR_UPLOAD_ERR = 2005 #头像上传失败


# 社交模块
SID_ERR = 3001 # SID参数错误
SWIPE_ERR = 3002 #滑动动作错误

class LogicException(Exception):
    """
    自定义逻辑异常
    调用者通过参数，传递错误码
    """

    def __init__(self,code):
        self.code = code


class LogicError(Exception):
    code = None


def gen_logic_error(name, code):
    return type(name, (LogicError,), {'code': code})


SidError = gen_logic_error('SidError', 3001)
SwipeError = gen_logic_error('SwipeError', 3002)
SwipeLimitError = gen_logic_error('SwipeLimitError', 3003)