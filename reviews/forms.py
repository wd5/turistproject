# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from reviews.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name','email','text')
