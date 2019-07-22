from django.db import models
from django.db.models import Q

from common import errors
from common.errors import LogicException
from social.managers import FriendManager


class Swiped(models.Model):
    MARK = (
        ('like', '喜欢'),
        ('dislike', '不喜欢'),
        ('superLike', '超级喜欢'),
    )

    uid = models.IntegerField()
    sid = models.IntegerField()
    mark = models.CharField(max_length=16, choices=MARK)
    created_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def swipe(cls, uid, sid, mark):
        marks = [m for m, _ in cls.MARK]
        if mark not in marks:
            # raise LogicException(errors.SWIPE_ERR)
            raise errors.SwipeError
        if cls.objects.filter(uid=uid, sid=sid, mark=mark):
            return False
        else:
            cls.objects.create(uid=uid, sid=sid, mark=mark)
            return True


    @classmethod
    def is_like(cls,uid,sid):
        return Swiped.objects.filter(uid=sid, sid=uid).exists()

    class Meta:
        db_table = 'swiped'





class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    objects = FriendManager()


    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return cls.objects.get_or_create(uid1=uid1, uid2=uid2)



    @classmethod
    def cencel_friends(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)

        cls.objects.filter(uid1=uid1,uid2=uid2).delete()
        pass

    @classmethod
    def friend_list(cls, uid):
        fid_list = []
        friends = cls.objects.filter(Q(uid1=uid) | Q(uid2=uid))

        for f in friends:
            fid = f.uid1 if uid == f.uid2 else f.uid2
            fid_list.append(fid)
        return fid_list

    class Meta:
        db_table = 'friends'
