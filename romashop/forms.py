# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from form_utils.widgets import ImageWidget
from romashop.models import Order, Customer, Product, Picture, Review, CallQuery


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('author')


class PictureAdminForm(forms.ModelForm):

    image = forms.FileField(widget=ImageWidget(width=140,height=140))

    class Meta:
        model = Picture


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        exclude = ('user')


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('comment', 'shipping_method', 'payment_method')


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('name','city','email','text')


class CallQueryForm(forms.ModelForm):

    class Meta:
        model = CallQuery
        fields = ('name','phone')
