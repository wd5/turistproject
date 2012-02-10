from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('romashop.views',
    url(r'^products/$', view='product_list', name='product_list'),
    url(r'^products/(?P<slug>\w+)/$', view='product_detail', name='product_detail'),
    url(r'^category/(?P<slug>\w+)/$', view='product_category', name='product_category'),
    url(r'^discounts/$', view='discount_list', name='discount_list'),
    url(r'^discounts/(?P<slug>\w+)/$', view='discount_detail', name='discount_detail'),

    url(r'^callquery/add/$', view='callquery_add', name='callquery_add'),
    url(r'^reviews/add/$', view='review_add', name='review_add'),

    url(r'^cart/add/(?P<product_id>\d+)/(?P<quantity>\d+)/$', view='add_to_cart', name='cart_add'),
    url(r'^cart/remove/(?P<product_id>\d+)/$', view='remove_from_cart', name='cart_remove'),
    url(r'^cart/clear/$', view='clear_cart', name='cart_clear'),

    url(r'^checkout/$', view='get_cart', name='cart_detail'),
)
