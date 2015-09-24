# -*- coding: utf-8 -*- vim:encoding=utf-8:
from django.conf.urls import patterns, url

from pops.views import pops_views

urlpatterns = patterns(
    '',
    url(r'^(?P<city>.+)/(?P<location>.+)$', pops_views.map_view, name='view'),
    url(r'^(?P<city>.+)/$', pops_views.map_view, name='view'),
    url(r'^$', pops_views.map_view, name='view'),
)
