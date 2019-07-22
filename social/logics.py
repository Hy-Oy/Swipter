import datetime

from django.core.cache import cache

from common import cache_keys, config, errors
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


def rewind(user):
    """
        撤销上一次滑动操作记录
        撤销上一次创建的好友关系
        :param user:
        :return:
    """
    key = cache_keys.SWIPE_LIMIT_PREFIX.format(user.id)

    swipe_times = cache.get(key,0)
    if swipe_times >= config.SWIPE_LIMIT:
        raise errors.SwipeLimitError

    swipe = Swiped.objects.filter(uid=user.id).latest("created_time")
    if swipe.mark in ['like', 'superlike']:
        Friend.cencel_friends(swipe.uid,swipe.sid)
    swipe.delete()
    now = datetime.datetime.now()
    timeout = 86400 - now.hour * 3600 - now.minute*60 - now.second

    cache.set(key, swipe_times+1, timeout)


def like_me(user):
    """
        查看喜欢过我的人，过滤掉已经存在的好友
        :param user:
        :return:
    """
    friend_list = Friend.friend_list(user.id)
    swipe_list = Swiped.objects.filter(sid=user.id, mark__in=['like','superlike']).exclude(
        uid__in=friend_list).only('uid')

    liked_me_uid_list = [s.uid for s in swipe_list]
    return liked_me_uid_list

