import datetime

from django.db import models

from libs.orm import ModelToDicMiXin

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



    phonenum = models.CharField(max_length=11, unique=True)
    nickname = models.CharField(max_length=16)
    sex = models.IntegerField(choices=SEXS, default=0)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avater = models.CharField(max_length=256)
    location = models.CharField(choices=LOCATIONS,max_length=32,default='gz')

    @property
    def age(self):
        date = datetime.date.today()
        age = date.year - self.birth_year
        age = age if date.month > self.birth_month and date.day > self.birth_day else age-1
        return age

    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(pk=self.id)

        return self._profile

    @property
    def to_dic(self):
        return {
            'uid': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'avater': self.avater,
            'location': self.location,
            'age': self.age,

        }

    class Meta:
        db_table = 'users'


    # def get_or_create_token(self):
    #     """
    #     为用户生成唯一的 token
    #     :return:
    #     """
    #     key = 'token:{}'.format(self.id)
    #
    #     token = cache.get(key)
    #
    #     if not token:
    #         token = 'token........1234123dsfsadfqesdf'
    #         cache.set(key, token, 24 * 60 * 60)
    #
    #     return token
class Profile(models.Model, ModelToDicMiXin):
    """
        location        目标城市
        min_distance    最小查找范围
        max_distance    最大查找范围
        min_dating_age  最小交友年龄
        max_dating_age  最大交友年龄
        dating_sex      匹配的性别

        auto_play       视频自动播放

        user.profile.location

        """
    location = models.CharField(max_length=32, choices=LOCATIONS, default='gz')
    min_distance = models.IntegerField(default=0)
    max_distance = models.IntegerField(default=10)
    min_dating_age = models.IntegerField(default=18)
    max_dating_age = models.IntegerField(default=81)
    dating_sex = models.IntegerField(choices=SEXS, default=0)

    auto_play = models.BooleanField(default=True)

    class Meta:
        db_table = 'profiles'
