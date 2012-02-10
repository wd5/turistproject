#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from romashop.managers import PublicManager, DiscountManager
from mptt.models import MPTTModel, TreeForeignKey

from datetime import datetime
import os
from PIL import Image
from sorl.thumbnail.main import DjangoThumbnail


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", blank=True, null=True)
    name = models.CharField("ФИО", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=50)
    city = models.CharField("Город", max_length=50)
    postcode = models.CharField("Индекс", max_length=50)
    address = models.CharField("Адрес", max_length=100)

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Product(models.Model):

    # publishing fields
    author = models.ForeignKey(User, verbose_name="Пользователь")
    is_published = models.BooleanField("Опубликовано", default=True)
    date_publish = models.DateTimeField("Дата публикации", default=datetime.now, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # core fields
    title = models.CharField("Название", max_length=70)
    slug = models.SlugField(max_length=70)
    category = models.ForeignKey('Category', verbose_name="Категория", blank=True, null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2)
    old_price = models.DecimalField(verbose_name='Старая цена', max_digits=12, decimal_places=2, blank=True, null=True)
    short_description = models.TextField("Описание", blank=True)
    long_description = models.TextField("Подробное описание", blank=True)

    objects = PublicManager()
    
    class Meta:
        ordering = ['-id']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __unicode__(self):
        return u"%s" % (self.title)

    def get_cover_image(self):
        cover = None
        image_list = [x for x in self.picture_set.all().order_by('position', 'id')]
        if len(image_list) > 0:
            cover = image_list[0]
            return cover.image
        else:
            return None

    def get_cover(self):
        cover = None
        image_list = [x for x in self.picture_set.all().order_by('position', 'id')]
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
        return ('product_detail', [unicode(self.slug)])


class Category(MPTTModel):

    name = models.CharField("Название", max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=50)
    parent = TreeForeignKey('self', verbose_name="Надкатегория", null=True, blank=True, related_name='children')
    position = models.PositiveIntegerField("Позиция", default=0)

    class MPTTMeta:
        order_insertion_by = ['position', 'name']

    class Meta:
        ordering = ['position', 'name']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __unicode__(self):
        return u"%s" % (self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('product_category', [unicode(self.slug)])


class Picture(models.Model):

    # publishing fields
    is_published = models.BooleanField("Опубликовано", default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # core fields
    product = models.ForeignKey(Product, verbose_name='Товар')
    image = models.ImageField("Изображение", upload_to='shop_pics/')
    title = models.CharField("Заголовок", max_length=100, blank=True)
    position = models.PositiveIntegerField("Позиция", default=0)

    objects = PublicManager()

    class Meta:
        ordering = ['position']
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __unicode__(self):
        return "%s" % (self.id)

    def image_thumb(self):
        if self.image:
            thumbnail1 = DjangoThumbnail(self.image, (120, 120))
            return u'<img src="%s"/>' % (thumbnail1.absolute_url)
            #return self.image.thumbnail_tag
        else:
            return ""
    image_thumb.short_description = "Изображение"
    image_thumb.allow_tags = True

    def save(self, size=(1280, 1280)):
        if not self.id and not self.image:
            return

        super(Picture, self).save()

        filename = os.path.join(settings.MEDIA_ROOT,self.image.name)
        image = Image.open(filename)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename, quality=95)

    @models.permalink
    def get_absolute_url(self):
        return ('romashop.views.photo_detail',[str(self.product.slug),str(self.id)])


SUBMITTED = 0
PAID = 1
SENT = 2
CLOSED = 3
CANCELED = 4
PAYMENT_FAILED = 5
PAYMENT_FLAGGED = 6


ORDER_STATES = [
    (SUBMITTED, "Новый"),
    (PAID, "Оплачен"),
    (SENT, "Отправлен"),
    (CLOSED, "Закрыт"),
    (CANCELED, "Отменен"),
    (PAYMENT_FAILED, "Оплата не прошла"),
    (PAYMENT_FLAGGED, "Оплата помечена"),
]


class Order(models.Model):

    customer = models.ForeignKey(Customer)
    number = models.CharField("Номер", max_length=70, default='0')
    date_created = models.DateTimeField("Дата создания", default=datetime.now())
    shipping_method = models.ForeignKey('ShippingMethod', verbose_name="Доставка", blank=True, null=True)
    payment_method = models.ForeignKey('PaymentMethod', verbose_name="Оплата", blank=True, null=True)
    status = models.PositiveSmallIntegerField("Статус", choices=ORDER_STATES, default=SUBMITTED)
    summary = models.DecimalField("Сумма", max_digits=12, decimal_places=2)
    comment = models.TextField("Дополнения", blank=True)

    def __unicode__(self):
        return u"[%s] %s" % (self.number, self.customer)

    def get_number(self, id):
        return u"%s" % ("N" + unicode(int(id) + 10000))

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderDetail(models.Model):

    order = models.ForeignKey(Order, related_name="items")
    product = models.ForeignKey(Product)
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    quantity = models.FloatField("Количество")
    total_price = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)

    def __unicode__(self):
        return u"%s - %s" % (self.order, self.product)

    class Meta:
        verbose_name = "Заказы-подпункт"
        verbose_name_plural = "Заказы-подпункты"


class PaymentMethod(models.Model):

    title = models.CharField("Название", max_length=70)
    tax = models.DecimalField("Значение", max_digits=12, decimal_places=2, default=0.0)
    is_percent = models.BooleanField("В процентах", default=False)
    position = models.PositiveIntegerField("Позиция в списке", default=0)

    def __unicode__(self):
        return u"%s" % (self.title)

    class Meta:
        ordering = ['position', 'title']
        verbose_name = "Метод оплаты"
        verbose_name_plural = "Методы оплаты"


class ShippingMethod(models.Model):

    title = models.CharField("Название", max_length=70)
    tax = models.DecimalField("Значение", max_digits=12, decimal_places=2, default=0.0)
    is_percent = models.BooleanField("В процентах", default=False)
    position = models.PositiveIntegerField("Позиция в списке", default=0)

    def __unicode__(self):
        return u"%s" % (self.title)

    class Meta:
        ordering = ['position', 'title']
        verbose_name = "Метод доставки"
        verbose_name_plural = "Методы доставки"


class Discount(models.Model):

    is_active = models.BooleanField("Активно", default=True)
    title = models.CharField("Название", max_length=70)
    slug = models.SlugField(unique=True, max_length=50)
    products = models.ManyToManyField(Product, verbose_name=u"Продукты")
    date_start = models.DateTimeField("Дата начала", default=datetime.now)
    date_end = models.DateTimeField("Дата окончания", default=datetime.now)
    tax = models.DecimalField("Значение", max_digits=12, decimal_places=2)
    is_percent = models.BooleanField("В процентах", default=False)

    objects = DiscountManager()

    def __unicode__(self):
        return u"%s" % (self.title)

    def is_now(self):
        date_now = datetime.now()
        if self.date_start < date_now and self.date_end > date_now:
            return True
        else:
            return False

    class Meta:
        ordering = ['date_end']
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


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


class CallQuery(models.Model):
    is_completed = models.BooleanField(verbose_name='Выполнен', default=False)
    name = models.CharField(verbose_name='Имя', max_length=100)
    phone = models.CharField(verbose_name='Телефон', max_length=100)
    datetime_added = models.DateTimeField(verbose_name='Время заказа', default=datetime.now())
    datetime_completed = models.DateTimeField(verbose_name='Время исполнения', blank=True, null=True)
    description = models.TextField(verbose_name='Замечания', blank=True)

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = 'Звонок'
        verbose_name_plural = 'Звонки'
        ordering = ["-datetime_added"]


class MarketingGroup(models.Model):

    name = models.CharField("Название", max_length=70, unique=True)
    slug = models.SlugField(unique=True, max_length=50)
    products = models.ManyToManyField(Product, verbose_name=u"Продукты")
    position = models.PositiveSmallIntegerField("Позиция", default=0)

    class Meta:
        verbose_name = 'Выделенный товар'
        verbose_name_plural = 'Выделенные товары'
        ordering = ["position"]

    def __unicode__(self):
        return u"%s" % (self.name)
