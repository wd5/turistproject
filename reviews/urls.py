# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('reviews.views',

    #url(r'^/$', view='reviews', name='reviews'),
    url(r'^add/$', view='review_add', name='review_add'),

)
