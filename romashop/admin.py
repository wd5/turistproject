# -*- coding: utf-8 -*-

from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from romashop.models import Product, Customer, Order, OrderDetail, Category, PaymentMethod, ShippingMethod, Discount

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(PaymentMethod)
admin.site.register(ShippingMethod)
admin.site.register(Discount)

