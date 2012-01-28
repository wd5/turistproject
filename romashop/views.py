# -*- coding: utf-8 -*-

# Create your views here.

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from cart import Cart
from romashop.models import Product, Category

def product_list(request):
    products = Product.objects.published()
    return direct_to_template(request, 'romashop/product_list.html', {'object_list': products})

def product_category(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.published().filter(category=category)
    return direct_to_template(request, 'romashop/product_list.html', {'object_list': products})

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return direct_to_template(request, 'romashop/product_detail.html', {'object': product})

def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    try:
        cart.add(product, product.price, quantity)
    except:
        pass
    return HttpResponseRedirect('/checkout/')

def clear_cart(request):
    cart = Cart(request)
    try:
        cart.clear()
    except:
        pass
    return HttpResponseRedirect('/checkout/')

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return HttpResponseRedirect('/checkout/')

def get_cart(request):
    return direct_to_template(request, 'romashop/cart_detail.html', dict(cart=Cart(request)))
