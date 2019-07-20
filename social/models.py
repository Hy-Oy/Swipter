from django.db import models


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
    def is_like(cls,uid,sid):
        return Swiped.objects.filter(uid=sid,sid=uid).exists()

    class Meta:
        db_table = 'swiped'


