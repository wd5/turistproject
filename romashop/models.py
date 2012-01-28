#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from fgallery.models import ALbum
    
class Item(models.Model):

    # publishing fields
    is_published = models.BooleanField(default=True)
    date_publish = models.DateTimeField(default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=70)

    # core fields
    images = models.ForeignKey('Album', blank=True, null=True)
    price = DecimalField(max_digits=12, decimal_places=2)
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    old_price = CurrencyField(verbose_name='Старая цена', blank=True, null=True)

    objects = AllManager()
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
