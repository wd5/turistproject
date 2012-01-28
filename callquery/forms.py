# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from callquery.models import CallQuery

class CallQueryForm(forms.ModelForm):
    class Meta:
        model = CallQuery
        fields = ('name','phone')
