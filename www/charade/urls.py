# coding: utf-8
################################### 
# 2016/1/21
# pc
###################################
from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.game_ready, name='game_ready'),
    # ex: /set/
    url(r'^set/$', views.game_set, name='game_set'),
    # ex: /set/12/play/
    url(r'^set/(?P<board_id>[0-9]+)/play/$', views.game_play, name='game_play'),
    # ex: /score/41/
    url(r'^score/(?P<wid>[0-9]+)/$', views.game_score, name='game_score'),
    # ex: /board/
    url(r'^board/$', views.game_board, name='game_board'),
    # ex: /explanation/41/
    url(r'^explanation/(?P<pk>[0-9]+)/$', views.Explanation.as_view(), name='explanation'),

    ### test use only
    # ex: /show/meta/
    #url(r'^show/meta/$',views.show_meta, name='show_meta')
]
