# coding: utf-8
################################### 
# 2016/2/15
# pc
###################################
from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    #################################### accounts
    #
    url(r'^login/$', auth_views.login,
            {'template_name': 'accounts/login.html'},
            name='login'),
    url(r'^logout/$', auth_views.logout,
            {'next_page': '/'},
            name='logout'),
]
