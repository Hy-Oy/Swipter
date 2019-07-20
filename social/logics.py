import datetime

from django.test import TestCase

# Create your tests here.
from social.models import Swiped
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
    ret = Swiped.objects.get_or_create(uid=uid, sid=sid, mark='like')
    if Swiped.is_like(uid,sid):
        print('----make friends-----')
    return ret