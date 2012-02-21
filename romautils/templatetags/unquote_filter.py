from django import template
from django.template.defaultfilters import stringfilter
from urllib import unquote_plus as unquote_func

register = template.Library()

@register.filter
@stringfilter
def unquote(value):
    return unquote_func(value.encode('utf8'))

