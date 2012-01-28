#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import Library, Node, Variable, TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType
from fgallery.models import ImageRelation

register = Library()

@register.filter
def class_name(value):
    return "%s-%s" % (value.__module__.split('.')[0], value.__class__.__name__.lower())

class MainImageNode(Node):

    def __init__(self, obj, varname):
        self.obj = obj
        self.varname = varname

    def render(self, context):
        context[self.varname] = None
        obj_type = ContentType.objects.get_for_model(self.obj.resolve(context))
        ph = ImageRelation.objects.filter(content_type__pk=obj_type.id,object_id=self.obj.resolve(context).id)
        if ph:
             context[self.varname] = ph[0]
        return ''

@register.tag
def get_main_image(parser, token):
    """
    Gets the main image for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax: {% get_main_image for [object] as [varname] %}
    """

    bits = token.contents.split()
    obj = parser.compile_filter(bits[2])
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_main_image tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_main_image tag must be 'as'"
    return MainImageNode(obj, bits[4])
