# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-03-23
# @ pc
###################################

from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Vocabulary(models.Model):
    en = models.CharField(_('English'), max_length=100, unique=True)
    zh = models.CharField(_('Chinese'), max_length=100)
    exp = models.TextField(_('Explanation'), max_length=200, null=True)

    dt = models.DateTimeField(_('Timestamp'), auto_now_add=True)

    def __str__(self):
        return self.en

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.dt <= now

    was_added_recently.admin_order_field = 'dt'
    was_added_recently.boolean = True
    was_added_recently.short_description = _('Added recently?')


class GameScoreBoard(models.Model):
    amount = models.IntegerField(_('Amount of words'), default=0)
    scores = models.IntegerField(_('Total Points'), default=0)
    dt_start = models.DateTimeField(_('Start'), auto_now_add=True)
    dt_end = models.DateTimeField(_('End'), auto_now=True)

    def __str__(self):
        return 'team %s' % self.id


class GameTemporaryTable(models.Model):
    board = models.ForeignKey(GameScoreBoard)
    en = models.CharField(_('English'), max_length=100)
    zh = models.CharField(_('Chinese'), max_length=100)
    exp = models.TextField(_('Explanation'), max_length=200, null=True)
    scores = models.IntegerField(_('Round points'), default=0)
    used = models.IntegerField(_('Already used?'), default=0)
    vid = models.IntegerField(_('Vocabulary ID'), default=0)


    def __str__(self):
        return self.en

