# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-02-18
# @ pc
###################################

from django.shortcuts import render, redirect, resolve_url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth import login

from .apps import AccountsConfig as conf
from .forms import RegistrationForm

# Create your views here.

def registration(request, registration_form=RegistrationForm):
    registered_user_redirect_to = conf.LOGIN_REDIRECT_URL
    post_registration_redirect = reverse('accounts:registration_finished')

    if request.user.is_authenticated():
        return redirect(registered_user_redirect_to)

    if not conf.REGISTRATION_IS_OPEN:
        return redirect(reverse('accounts:registration_closed'))

    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            if conf.REGISTRATION_IS_AUTOLOGIN and conf.IS_AUTOACTIVE:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            return redirect(post_registration_redirect)
    else:
        form = registration_form()

    context = {
        'thisform': form,
    }

    return render(request, 'accounts/registration.html', context)


def registration_closed(request):
    return render(request, 'accounts/registration_closed.html')


def registration_finished(request):
    return render(request, 'accounts/registration_finished.html')
