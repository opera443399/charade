# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-02-16
# @ pc
###################################

from django.shortcuts import redirect, resolve_url
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site

from .apps import AccountsConfig as conf
from .forms import RegistrationForm

# Create your views here.

def registration(request,
             template_name='accounts/registration.html',
             registration_form=RegistrationForm,
             registered_user_redirect_to=None,
             post_registration_redirect=None,
             current_app=None,
             extra_context=None):

    if registered_user_redirect_to is None:
        registered_user_redirect_to = conf.LOGIN_REDIRECT_URL

    if request.user.is_authenticated():
            return redirect(registered_user_redirect_to)

    if not conf.REGISTRATION_IS_OPEN:
        return redirect(reverse('accounts:registration_closed'))

    if post_registration_redirect is None:
        post_registration_redirect = reverse('accounts:registration_finished')

    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            if conf.REGISTRATION_IS_AUTOLOGIN:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            return redirect(post_registration_redirect)
    else:
        form = registration_form()

    current_site = get_current_site(request)

    context = {
        'form': form,
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Register'),
    }

    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def registration_closed(request,
                        template_name='accounts/registration_closed.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': _('Registration closed'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def registration_finished(request,
                          template_name='accounts/registration_finished.html',
                          current_app=None,
                          extra_context=None):
    context = {
        'login_url': resolve_url(conf.LOGIN_URL),
        'title': _('Registration finished'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
