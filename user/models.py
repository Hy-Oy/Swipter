from django.db import models


class User(models.Model):
    """
        phonenum 手机号
        nickname 昵称
        sex 性别
        birth_year 出生年
        birth_month 出生月
        birth_day 出生日
        avatar 个人形象
        location 常居地
    """

    SEXS = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )

    LOCATIONS = (
        ('bj', '北京'),
        ('sh', '上海'),
        ('hz', '杭州'),
        ('sz', '深圳'),
        ('cd', '成都'),
        ('gz', '广州'),
    )

    phonenum = models.CharField(max_length=11, unique=True)
    nickname = models.CharField(max_length=16)
    sex = models.IntegerField(choices=SEXS, default="0")
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avater = models.CharField(max_length=256)
    location = models.CharField(choices=LOCATIONS,max_length=32,default='gz')

    class Meta:
        db_table = 'users'