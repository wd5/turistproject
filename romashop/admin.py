# -*- coding: utf-8 -*-

from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from romashop.models import Product, Customer, Order, OrderDetail, Category, PaymentMethod, ShippingMethod, Discount, Picture, Review, CallQuery, MarketingGroup

from romashop.forms import ProductAdminForm, PictureAdminForm


class OrderDetailInline(admin.TabularInline):

    model = OrderDetail


class OrderAdmin(admin.ModelAdmin):

    inlines = [OrderDetailInline,]
    list_display = ['number', 'customer', 'date_created', 'summary', 'status']


class PictureInline(admin.TabularInline):

    model = Picture
    form = PictureAdminForm
    fields = ('image', 'title', 'position')


class ProductAdmin(admin.ModelAdmin):

    list_display = ['get_cover', 'title', 'price', 'old_price', 'is_published']
    list_editable = ['title', 'price', 'old_price', 'is_published']
    inlines = [PictureInline,]
    form = ProductAdminForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


class CategoryAdmin(MPTTModelAdmin):

    list_display = ['name', 'position']
    list_editable = ['position']

    def save_formset(self, request, form, formset, change):
        Category.tree.rebuild()


class ReviewAdmin(admin.ModelAdmin):

    list_display = ['name', 'datetime_added']


class DiscountAdmin(admin.ModelAdmin):

    list_display = ['title', 'date_start', 'date_end', 'is_now', 'is_active']
    list_editable = ['is_active']
    filter_horizontal = ('products',)


class MarketingGroupAdmin(admin.ModelAdmin):

    list_display = ['name', 'position']
    list_editable = ['position']
    filter_horizontal = ('products',)


class CallQueryAdmin(admin.ModelAdmin):

    list_display = ['__unicode__', 'phone', 'datetime_added', 'is_completed']
    actions = ['complete']

    def complete(self, request, queryset):
        rows_updated = queryset.update(is_completed=True, datetime_completed=datetime.now())
        if rows_updated == 1:
           message_bit = '1 звонок был отмечен'
        else:
           message_bit = '%s звонков было отмечено' % rows_updated
        self.message_user(request, '%s как выполненные.' % message_bit)
    complete.short_description = u'Пометить как выполненное'


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PaymentMethod)
admin.site.register(ShippingMethod)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(CallQuery, CallQueryAdmin)
admin.site.register(MarketingGroup, MarketingGroupAdmin)

