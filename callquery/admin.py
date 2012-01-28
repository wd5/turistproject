# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from callquery.models import CallQuery
from datetime import datetime

class CallQueryAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'phone', 'datetime_added', 'completed']
    actions = ['complete']

    def complete(self, request, queryset):
        rows_updated = queryset.update(completed=True, datetime_completed=datetime.now())
        if rows_updated == 1:
           message_bit = "1 звонок был отмечен"
        else:
           message_bit = "%s звонков было отмечено" % rows_updated
        self.message_user(request, "%s как выполненные." % message_bit)
    complete.short_description = u'Пометить как выполненное'

admin.site.register(CallQuery, CallQueryAdmin)
