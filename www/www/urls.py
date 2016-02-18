"""www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from charade import views as charade_views

urlpatterns = [
    url(r'^$', charade_views.index, name='index'),

    #################################### apps
    #
    url(r'^accounts/', include('accounts.urls')),
    url(r'^charade/', include('charade.urls')),
    url(r'^polls/', include('polls.urls')),

    #################################### admin
    #
    url(r'^admin/', include(admin.site.urls)),

    #################################### i18n
    #
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
