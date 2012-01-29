# -*- coding: utf-8 -*-

# Create your views here.

from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseRedirect
from cart import Cart
from romashop.models import Product, Category, Customer, OrderDetail, Review
from romashop.forms import CustomerForm, OrderForm, ReviewForm, CallQueryForm


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


def review_add(request):

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ReviewForm()

    return direct_to_template(request, 'romashop/review_form.html',{'form':form})


def callquery_add(request):

    if request.method == 'POST':
        form = CallQueryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = CallQueryForm()

    return direct_to_template(request, 'romashop/callquery_form.html',{'form':form})


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

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        order_form = OrderForm(request.POST)
        if form.is_valid():

            # SAVE CUSTOMER
            new_customer = form.save(commit=False)
            if request.user.is_authenticated():
                new_customer.user = request.user
            new_customer.save()

            if order_form.is_valid():

                # SAVE ORDER
                new_order = order_form.save(commit=False)
                new_order.customer = new_customer
                new_order.summary = cart.summary()
                new_order.save()
                new_order.number = new_order.get_number(new_order.id)
                new_order.save()

                # SAVE CART TO ORDER DETAIL
                for item in cart:
                    new_item = OrderDetail()
                    new_item.order = new_order
                    new_item.product = item.product
                    new_item.price = item.unit_price
                    new_item.quantity = item.quantity
                    new_item.total_price = item.total_price
                    new_item.save()
                cart.clear()

                return direct_to_template(request, 'romashop/order_thanks.html',{'object':new_order})

    else:
        form = CustomerForm(instance=customer)
        order_form = OrderForm()

    return direct_to_template(request, 'romashop/cart_detail.html', {'cart':cart, 'form':form, 'order_form':order_form})
