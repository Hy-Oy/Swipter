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