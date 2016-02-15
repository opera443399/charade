# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-02-15
# @ pc
###################################

from django.conf.urls import url
from . import views

app_name = 'charade'
urlpatterns = [
    #################################### /charade/xxx
    #
    url(r'^$', views.game_ready, name='game_ready'),
    url(r'^set/$', views.game_set, name='game_set'),
    url(r'^set/(?P<board_id>[0-9]+)/play/$', views.game_play, name='game_play'),
    url(r'^score/(?P<wid>[0-9]+)/$', views.game_score, name='game_score'),
    url(r'^board/$', views.game_board, name='game_board'),
    url(r'^explanation/(?P<pk>[0-9]+)/$', views.Explanation.as_view(), name='explanation'),

    #################################### /show/xxx
    # simple test
    url(r'^show/about/$', views.show_about, name='show_about'),
    url(r'^show/time/$', views.show_time, name='show_time'),
    #url(r'^show/meta/$', views.show_meta, name='show_meta'),
]
