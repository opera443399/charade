# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-02-16
# @ pc
###################################

from __future__ import unicode_literals

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/'
    REGISTRATION_IS_OPEN = True
    REGISTRATION_IS_AUTOLOGIN = True
    NEET_VERIFY_EMAIL = False
    PASSWORD_LEN_MIN = 5
    PASSWORD_LEN_MAX = None
    PASSWORD_COMPLEXITY_CHECK = True
    PASSWORD_POLICY = {
        'UPPER': 1,       # Uppercase 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        'LOWER': 1,       # Lowercase 'abcdefghijklmnopqrstuvwxyz'
        'DIGITS': 1,      # Digits '0123456789'
        'PUNCTUATION': 0  # Punctuation """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    }
    EMAIL_DOMAIN_VALIDATE = True
    EMAIL_DOMAINS_BLACKLIST = []
    EMAIL_DOMAINS_WHITELIST = []
