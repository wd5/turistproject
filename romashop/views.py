# -*- coding: utf-8 -*-

# Create your views here.

from django.views.generic.simple import direct_to_template
from cart import Cart
from romashop.models import Product

def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product, product.price, quantity)

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)

def get_cart(request):
    return direct_to_template('romashop/cart.html', dict(cart=Cart(request)))
