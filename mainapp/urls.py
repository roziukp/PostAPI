from django.conf.urls import url
from .apiviews import (UserRegistration, UserLogin, PostCreateView, Likes, Unlike, PostListView)
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    url(r'^registration/$', UserRegistration.as_view(), name='registration'),
    url(r'^login/$', UserLogin.as_view(), name='user_login'),
    url(r'^post_create/$', PostCreateView.as_view(), name='post_create'),
    url(r'^post_list/$', PostListView.as_view(), name='post_list'),
    url(r'^refresh_token/$', refresh_jwt_token, name='refresh_jwt_token'),
    url(r'^post/(?P<pk>[\d])/like/$', Likes.as_view(), name='like_view'),
    url(r'^post/(?P<pk>[\d])/dislike/$', Unlike.as_view(), name='dislike_view'),
]
