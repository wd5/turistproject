# -*- coding: utf-8 -*-

# Create your views here.

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from cart import Cart
from romashop.models import Product, Category, Customer
from romashop.forms import CustomerForm, OrderForm

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

    cart = Cart(request)

    if request.user.is_authenticated():
        try:
            customer = Customer.objects.get(user=request.user)
        except:
            customer = None
    else:
        customer = None

    if request.method == 'POST': # If the form has been submitted...
        form = CustomerForm(request.POST) # A form bound to the POST data
        order_form = OrderForm(request.POST)
        if form.is_valid(): # All validation rules pass
            cstm = form.save(commit=False)
            if request.user.is_authenticated():
                cstm.user = request.user
            cstm.save()
            if order_form.is_valid():
                oform = order_form.save(commit=False)
                oform.customer = cstm
                oform.summary = cart.summary()
                oform.save()
                cart.clear()
                return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = CustomerForm(instance=customer) # An unbound form
        order_form = OrderForm()

    return direct_to_template(request, 'romashop/cart_detail.html', {'cart':cart, 'form':form, 'order_form':order_form})
