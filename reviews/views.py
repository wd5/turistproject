# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from reviews.models import Review
from reviews.forms import ReviewForm

def review_add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ReviewForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = ReviewForm() # An unbound form

    return direct_to_template(request, 'reviews/review_form.html',{'form':form})
