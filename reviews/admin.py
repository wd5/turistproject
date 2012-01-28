# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from reviews.models import Review
from datetime import datetime

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'name', 'datetime_added']

admin.site.register(Review, ReviewAdmin)
