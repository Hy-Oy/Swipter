import datetime


from social.models import Swiped, Friend
from user.models import User


def recommend_users(user):
    today = datetime.date.today()

    max_year = today.year - user.profile.min_dating_age

    min_year = today.year - user.profile.max_dating_age

    swiped_users = Swiped.objects.filter(uid=user.id).only('sid')

    swiped_sid_list = [s.sid for s in swiped_users]

    rec_users = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__gte=min_year,
        birth_year__lte=max_year,
    ).exclude(id__in=swiped_sid_list)[:20]
    return rec_users


def like_someone(uid, sid):
    """
        喜欢操作，如果被滑动人，喜欢当前用户，则创建好友关系
        :param uid:
        :param sid:
        :return:
    """
    ret = Swiped.swipe(uid=uid, sid=sid, mark='like')
    # 如果 sid 喜欢 uid，则进行加好友操作
    if ret and Swiped.is_like(uid, sid):
        _, created = Friend.make_friends(sid, uid)
        # 发送 匹配好友成功的 推送消息
        return created
    return False


def superlike_someone(uid, sid):
    """
        超级喜欢操作，如果被滑动人，喜欢当前用户，则创建好友关系
        :param uid:
        :param sid:
        :return:
        """
    ret = Swiped.swipe(uid=uid, sid=sid, mark='superlike')

    if ret and Swiped.is_like(uid, sid):
        _, created = Friend.objects.make_friends(sid, uid)
        return created
    return False