# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-03-03
# @ pc
###################################

from django.conf.urls import url

from . import views

app_name = 'upload'
urlpatterns = [
    #################################### upload
    #
    url(r'^$', views.PictureCreateView.as_view(), name='pic-add'),
    url(r'^delete/(?P<pk>\d+)/$', views.PictureDeleteView.as_view(), name='pic-delete'),
    url(r'^list/$', views.PictureListView.as_view(), name='pic-list'),
]