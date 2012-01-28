#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from models import Photo, Album
from form_utils.widgets import ImageWidget
from django.contrib.contenttypes import generic


class PhotoForm(forms.ModelForm):
    image = forms.FileField(widget=ImageWidget(width=140,height=140))
    class Meta:
        model = Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    form = PhotoForm
    fields = ('image', 'title')

class AlbumAdmin(admin.ModelAdmin):
    #exclude = ["author"]
    raw_id_fields = ["cover"]
    list_display = ["get_cover", "title", "is_published"]
    list_editable = ["title", "is_published"]    
    inlines = [PhotoInline,]

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["image_thumb", "title", "album"]
    list_editable = ["title", "album"]
    list_filter = ["album"]
    #prepopulated_fields = {"slug": ("title",)}

    fieldsets = [
        (None,               {'fields': ['is_published','album','image','title']}),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
