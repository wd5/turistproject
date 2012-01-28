# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from romashop.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name','email','text')
