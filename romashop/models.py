#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from fgallery.models import Album
from romashop.managers import PublicManager
from mptt.models import MPTTModel, TreeForeignKey
from datetime import datetime


class Customer(models.Model):

    author = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField("ФИО", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=50)
    city = models.CharField("Город", max_length=50)
    postcode = models.CharField("Индекс", max_length=50)
    address = models.CharField("Адрес", max_length=100)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Product(models.Model):

    # publishing fields
    author = models.ForeignKey(User, verbose_name="Пользователь")
    is_published = models.BooleanField(default=True)
    date_publish = models.DateTimeField("Дата публикации", default=datetime.now, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=70)

    # core fields
    title = models.CharField("Название", max_length=70)
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2)
    old_price = models.DecimalField(verbose_name='Старая цена', max_digits=12, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey('Category', verbose_name="Категория", blank=True, null=True)
    images = models.ForeignKey(Album, verbose_name="Изображения", blank=True, null=True)
    short_description = models.TextField("Описание", blank=True)
    long_description = models.TextField("Подробное описание", blank=True)

    objects = PublicManager()
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __unicode__(self):
        return "%s" % (self.title)


class Category(MPTTModel):

    name = models.CharField("Название", max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=50)
    parent = TreeForeignKey('self', verbose_name="Надкатегория", null=True, blank=True, related_name='children')
    position = models.PositiveIntegerField("Позиция", default=0)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __unicode__(self):
        return "%s" % (self.name)


SUBMITTED = 0
PAID = 1
SENT = 2
CLOSED = 3
CANCELED = 4
PAYMENT_FAILED = 5
PAYMENT_FLAGGED = 6


ORDER_STATES = [
    (SUBMITTED, "Внесен"),
    (PAID, "Оплачен"),
    (SENT, "Отправлен"),
    (CLOSED, "Закрыт"),
    (CANCELED, "Отменен"),
    (PAYMENT_FAILED, "Оплата не прошла"),
    (PAYMENT_FLAGGED, "Оплата отмечена"),
]


class Order(models.Model):

    customer = models.ForeignKey(Customer)
    number = models.CharField("Номер", max_length=70)
    date_created = models.DateTimeField("Дата создания", auto_now_add=True)
    shipping_method = models.ForeignKey('ShippingMethod', verbose_name="Доставка", blank=True, null=True)
    payment_method = models.ForeignKey('PaymentMethod', verbose_name="Оплата", blank=True, null=True)
    status = models.PositiveSmallIntegerField("Статус", choices=ORDER_STATES, default=SUBMITTED)
    summary = models.DecimalField("Сумма", max_digits=12, decimal_places=2)

    def __unicode__(self):
        return "[%s] %s" % (self.number, self.customer)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderDetail(models.Model):

    order = models.ForeignKey(Order, related_name="items")
    product = models.ForeignKey(Product, blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    product_amount = models.FloatField("Количество", blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.order, self.product)

    class Meta:
        verbose_name = "Заказ-товар"
        verbose_name_plural = "Заказы-товары"


class PaymentMethod(models.Model):

    title = models.CharField("Номер", max_length=70)
    position = models.PositiveIntegerField(default=0)
    tax = models.DecimalField("Значение", max_digits=12, decimal_places=2)
    is_percent = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = "Метод оплаты"
        verbose_name_plural = "Методы оплаты"


class ShippingMethod(models.Model):

    title = models.CharField("Номер", max_length=70)
    position = models.PositiveIntegerField(default=0)
    tax = models.DecimalField("Значение", max_digits=12, decimal_places=2)
    is_percent = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = "Метод доставки"
        verbose_name_plural = "Методы доставки"


class Discount(models.Model):

    title = models.CharField("Название", max_length=70)
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    is_global = models.BooleanField("На все продукты", default=False)
    date_start = models.DateTimeField("Дата начала", default=datetime.now)
    date_end = models.DateTimeField("Дата окончания", default=datetime.now)
    tax = models.DecimalField("Значение", max_digits=12, decimal_places=2)
    is_percent = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
