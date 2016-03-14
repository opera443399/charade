# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-03-14
# @ pc
###################################

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'upload'
urlpatterns = [
    #################################### upload
    #
    url(r'^$', login_required(views.PictureCreateView.as_view()), name='pic-add'),
    url(r'^add$', login_required(views.PictureCreateView.as_view()), name='pic-add'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(views.PictureDeleteView.as_view()), name='pic-delete'),
    url(r'^gallary/$', views.PictureListView.as_view(), name='pic-list'),
]
