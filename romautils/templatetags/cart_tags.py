from django.db.models import get_model
from django.template import Library, Node
from django.contrib.sites.models import Site
from django.template import TemplateSyntaxError, Variable
from cart import Cart

register = Library()

class CartNode(Node):

    def __init__(self, varname):
        self.request = Variable('request')
        self.varname = varname
        
    def render(self, context):
        rqst = self.request.resolve(context)
        cart = Cart(rqst)
        context[self.varname] = cart
        return ''

def get_cart(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest_comments tag must be 'as'"
    return CartNode(bits[2])
    
get_cart = register.tag(get_cart)
