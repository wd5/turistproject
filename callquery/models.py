# -*- coding: utf-8 -*-

from django.db import models

class CallQuery(models.Model):
    name = models.CharField(verbose_name='Ваше имя', max_length=100)
    phone = models.CharField(verbose_name='Телефон', max_length=100)
    datetime_added = models.DateTimeField(verbose_name='Время заказа', auto_now_add=True)
    datetime_completed = models.DateTimeField(verbose_name='Время исполнения', blank=True, null=True)
    completed = models.BooleanField(verbose_name='Выполнен', default=False)
    description = models.TextField(verbose_name='Описание', blank=True)

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = 'Заказ звонка'
        verbose_name_plural = 'Заказы звонков'
        ordering = ["-datetime_added"]
