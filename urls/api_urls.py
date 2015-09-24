# -*- coding: utf-8 -*- vim:encoding=utf-8:
from django.conf.urls import patterns, url
from pops.views import api

urlpatterns = patterns(
    '',
    url(r'^locations/(?P<location>[\w|\W]+)/$', api.location, name='location'),
    url(r'^(?P<city>[\w|\W]+)/$', api.pops, name='pops'),
    url(r'^$', api.pops, name='pops'),
)
