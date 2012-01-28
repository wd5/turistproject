# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Item
from shop_simplecategories.admin import ProductWithCategoryForm

class ItemForm(ProductWithCategoryForm):
    class Meta(object):
        model = Item

class ItemAdmin(admin.ModelAdmin):
    form = ItemForm

admin.site.register(Item, ItemAdmin)

