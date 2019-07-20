from common import errors
from libs.http import render_json
from social import logics


def like(request):
    user = request.user
    sid = request.POST.get("sid")
    if sid is None:
        return render_json(code=errors.SID_ERR)
    sid = int(sid)
    matched = logics.like_someone(user.id, sid)
    return render_json()


def recommend(request):
    user = request.user

    rec_users = logics.recommend_users(user)

    users = [u.to_dic for u in rec_users]
    return render_json(data=users)


def dislike(request):
    return None


def superlike(request):
    return None


def remind(request):
    return None


def me(request):
    return None