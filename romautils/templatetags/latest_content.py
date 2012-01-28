from django.db.models import get_model
from django.template import Library, Node
from django.contrib.sites.models import Site
from django.template import TemplateSyntaxError

register = Library()

class LatestContentNode(Node):

    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
        
    def render(self, context):
        site = Site.objects.get_current()
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest_comments tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
    
get_latest = register.tag(get_latest)

class LatestPublicContentNode(Node):

    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
        
    def render(self, context):
        site = Site.objects.get_current()
        context[self.varname] = self.model._default_manager.published()[:self.num]
        return ''

def get_latest_public(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest_comments tag must be 'as'"
    return LatestPublicContentNode(bits[1], bits[2], bits[4])
    
get_latest_public = register.tag(get_latest_public)
