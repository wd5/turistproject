# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from romashop.managers import PublicManager
from datetime import datetime


class Review(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", blank=True, null=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    datetime_added = models.DateTimeField(verbose_name='Дата и время', default=datetime.now())

    name = models.CharField(verbose_name='Имя', max_length=100)
    text = models.TextField(verbose_name='Отзыв')
    email = models.CharField(verbose_name='E-mail', max_length=100, blank=True)
    link = models.CharField(verbose_name='Ссылка', max_length=100, blank=True)
    image = models.ImageField("Изображение", upload_to='reviews/', blank=True, null=True)

    objects = PublicManager()

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ["-datetime_added"]
