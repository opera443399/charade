# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-03-23
# @ pc
###################################

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Picture(models.Model):
    file = models.ImageField(upload_to='pictures/%Y/%m/%d')
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)
