# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from callquery.models import CallQuery
from callquery.forms import CallQueryForm

def callquery(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CallQueryForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = CallQueryForm() # An unbound form

    return direct_to_template(request, 'callquery/callquery_form.html',{'form':form})
