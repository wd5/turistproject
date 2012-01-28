from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from form_utils.widgets import ImageWidget
from models import Photo

class PhotoForm(forms.ModelForm):
    #id = forms.IntegerField(widget=forms.HiddenInput())
    image = forms.ImageField(widget=ImageWidget(width=140,height=140))
    #title = forms.CharField()
    #seo_title = forms.CharField()
    
    class Meta:
        model = Photo
