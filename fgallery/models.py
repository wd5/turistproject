#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime

from tagging.fields import TagField
#from sorl.improved.fields import ImprovedImageWithThumbnailsField
from django.contrib.auth.models import User
from fevents.models import Event
from fgallery.managers import PublicManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.conf import settings 
from PIL import Image
import os
from sorl.thumbnail.main import DjangoThumbnail


class Album(models.Model):
    # publishing fields
    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=True)
    date_publish = models.DateTimeField(default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=70)

    # core fields
    cover = models.ForeignKey('Photo', related_name='album_cover', blank=True, null=True)
    date = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=70)
    description = models.TextField(blank=True)
    position = models.IntegerField(default=0)

    enable_comments = models.BooleanField(default=True)

    objects = PublicManager()

    class Meta:
        verbose_name = "альбом"
        verbose_name_plural = "альбомы"

    def __unicode__(self):
        dt = unicode(self.date)[:10]
        return "[%s]-%s" % (dt, self.title)

    def images(self):
        lst = [x.image for x in self.photo_set.all().order_by('date')]
        lst = ["%s" % (x.thumbnail_tag) for x in lst]
        #lst = ["<a href='/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
        return ", <br>".join(lst)
    images.allow_tags = True

    def get_cover_image(self):
        cover = self.cover
        if not cover:
            image_list = [x for x in self.photo_set.all().order_by('id')]
            if len(image_list) > 0:
                cover = image_list[0]
        return cover.image

    def get_cover(self):
        if self.cover:
            cover = self.cover.image
        else:
            image_list = [x for x in self.photo_set.all().order_by('id')]
            if len(image_list) > 0:
                cover = image_list[0].image
        if cover:
            thumbnail1 = DjangoThumbnail(cover, (120, 120))
            return u'<img src="%s"/>' % (thumbnail1.absolute_url)
        else:
            return None
    get_cover.allow_tags = True

    @models.permalink
    def get_absolute_url(self):
        return ('fgallery.views.album1',[str(self.id)])

class Photo(models.Model):
    # publishing fields
    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=True)
    date_publish = models.DateTimeField(default=datetime.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # core fields
    album = models.ForeignKey(Album, blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=70)
    description = models.TextField(blank=True)
    position = models.IntegerField(default=0)

    enable_comments = models.BooleanField(default=True)

    objects = PublicManager()

    """
    image = ImprovedImageWithThumbnailsField(
        upload_to='photos/',
        max_width=800, max_height=800, # Thumbnail for admin site.
        thumbnail={
            'size': (120, 120),
            #'options': ('crop','upscale'),
        },
        extra_thumbnails={
            'main': {
                'size': (200, 200),
                #'options': ('crop','upscale'),
            }
        })
    """


    #slug = models.SlugField(unique=True, max_length=70, blank=True, null=True)
    #tags = TagField()

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фотографии"

    def __unicode__(self):
        dt = unicode(self.date)[:10]
        return "%s-[%s]-%s" % (self.id, dt, self.title)

    def image_thumb(self):
        if self.image:
            thumbnail1 = DjangoThumbnail(self.image, (120, 120))
            return u'<img src="%s"/>' % (thumbnail1.absolute_url)
            #return self.image.thumbnail_tag
        else:
            return ""
    image_thumb.short_description = "Фото"
    image_thumb.allow_tags = True

    def save(self, size=(1280, 1280)):
        """
        Save Photo after ensuring it is not blank. Resize as needed.
        """
        if not self.id and not self.image:
            return

        super(Photo, self).save()

        filename = os.path.join(settings.MEDIA_ROOT,self.image.name)
        image = Image.open(filename)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename, quality=95)

    def get_next_album_image(self, image):
        #previous = Photo.objects.filter(album=image.album).filter(id__lt=image.id)
        pass

    @models.permalink
    def get_absolute_url(self):
        return ('fgallery.views.photo_detail',[str(self.album.id),str(self.id)])


