# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-02-16
# @ pc
###################################

from django import forms, template

register = template.Library()


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)

