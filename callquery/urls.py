# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('callquery.views',

    url(r'^add/$', view='callquery', name='callquery'),

)
