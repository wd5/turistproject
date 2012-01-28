# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from reviews.managers import PublicManager

class Review(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    is_published = models.BooleanField(default=True)

    name = models.CharField(verbose_name='ФИО', max_length=100)
    email = models.CharField(verbose_name='E-mail', max_length=100, blank=True)
    datetime_added = models.DateTimeField(verbose_name='Время заказа', auto_now_add=True)
    text = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)

    objects = PublicManager()

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ["-datetime_added"]
