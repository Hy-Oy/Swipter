from django.urls import path

from social import apis

urlpatterns = [
    path('like',apis.like),
    path('recommend', apis.recommend),
    path('dislike', apis.dislike),
    path('superlike', apis.superlike),
    path('remind', apis.remind),
    path('like-me', apis.me),

]