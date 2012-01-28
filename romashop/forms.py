# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from romashop.models import Order, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ('user')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('shipping_method', 'payment_method')
