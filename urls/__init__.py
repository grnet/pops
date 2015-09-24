# -*- coding: utf-8 -*- vim:encoding=utf-8:
from django.conf.urls.defaults import include, patterns
from pops.urls import pops_urls

urlpatterns = patterns(
    'pops.views',
    (r'^', include(pops_urls, namespace='pops')),
)
