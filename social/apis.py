from common import errors
from libs.http import render_json
from social import logics
from social.models import Swiped
from user.models import User


def like(request):
    user = request.user
    sid = request.POST.get("sid")
    if sid is None:
        return render_json(code=errors.SID_ERR)
    sid = int(sid)
    matched = logics.like_someone(user.id, sid)
    return render_json(data={'matched': matched})


def recommend(request):
    user = request.user

    rec_users = logics.recommend_users(user)

    users = [u.to_dic for u in rec_users]
    return render_json(data=users)


def dislike(request):
    user = request.user
    sid = request.POST.get("sid")

    if sid is None:
        return render_json(code=errors.SID_ERR)

    sid = int(sid)

    Swiped.swipe(uid=user.id, sid=sid, mark='dislike')

    return render_json()


def superlike(request):
    user = request.user
    sid = request.POST.get("sid")
    if sid is None:
        return render_json(code=errors.SID_ERR)
    sid = int(sid)
    matched = logics.superlike_someone(user.id, sid)
    return render_json(data={'matched': matched})



def remind(request):
    """
        反悔接口
        :param request:
        :return:
        """
    user = request.user

    logics.rewind(user)

    return render_json()


def like_me(request):
    user = request.user

    uid_list = logics.like_me(user)
    like_me_user_list = User.objects.filter(id__in=uid_list)

    users = [u.to_dic for u in like_me_user_list]

    return render_json(data=users)