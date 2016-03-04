# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-03-04
# @ pc
###################################

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView

from .models import Picture

# Create your views here.


class PictureCreateView(CreateView):
    model = Picture
    fields = "__all__"
    success_url = reverse_lazy('upload:pic-list')


class PictureDeleteView(DeleteView):
    model = Picture
    context_object_name = "this_pic"
    success_url = reverse_lazy('upload:pic-list')


class PictureListView(ListView):
    model = Picture
    context_object_name = "all_pics"
