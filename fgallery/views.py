#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fgallery.models import Album, Photo, Video
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404
from tagging.models import Tag, TaggedItem
from django.views.generic import date_based, list_detail
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
import urllib

def albums(request):
    album_list = Album.objects.filter(is_published=True).order_by('-date_mod')
    video_list = Video.objects.published()
    return direct_to_template(request, 'fgallery/album_list.html', {'album_list': album_list, 'video_list': video_list})

def album1(request, falbum_id):
    albumres = Album.objects.get(id=falbum_id) #.all()#.order_by('-pub_date')[:10]
    return direct_to_template(request, 'fgallery/album_detail.html', {'albumres': albumres})

from django.forms.models import inlineformset_factory
from forms import PhotoForm

@staff_member_required
def album_edit(request, falbum_id):
    
    album = Album.objects.get(id=falbum_id)
    PhotoFormSet = inlineformset_factory(Album, Photo, form=PhotoForm, fields=('image', 'title', 'seo_title'), extra=0)
    
    if request.method == 'POST':
        formset = PhotoFormSet(request.POST, request.FILES, instance=album)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            #for form in formset.forms:
            formset.save()

            return HttpResponseRedirect('/gallery/')
    else:
        formset = PhotoFormSet(instance=album)
        
    return direct_to_template(request, 'fgallery/album_edit.html', {'album': album, 'formset': formset})

def album1c(request, falbum_id):
    albumres = Album.objects.get(id=falbum_id) #.all()#.order_by('-pub_date')[:10]
    return direct_to_template(request, 'fgallery/album_comments.html', {'albumres': albumres})

def photo1(request, fphoto_id):
    photores = Photo.objects.get(id=fphoto_id)
    return redirect(photores, permanent=True)

def photo_detail(request, falbum_id, fphoto_id):
    photores = Photo.objects.get(id=fphoto_id)
    if not request.user.is_staff:
        photores.view_count += 1
        photores.save()

    #previd = int(fphoto_id) - 1
    try:
        #photoprev = Photo.objects.get(id=previd)
        photoprev = photores.get_previous_by_date(album__exact=photores.album)
    except:
        photoprev = None
    if photoprev:
        if photoprev.album != photores.album:
            photoprev = None

    #nextid = int(fphoto_id) + 1
    try:
        #photonext = Photo.objects.get(id=nextid)
        photonext = photores.get_next_by_date(album__exact=photores.album)
    except:
        photonext = None
    if photonext:
        if photonext.album != photores.album:
            photonext = None

    return direct_to_template(request, 'fgallery/photo_detail.html', {'photores': photores, 'photoprev': photoprev, 'photonext': photonext, 'next': photores.get_absolute_url() })


def tag_detail(request, slug, template_name = 'fgallery/tag_detail.html', **kwargs):
    """
    Tag detail

    Template: ``fgallery/tag_detail.html``
    Context:
    object_list
    List of posts specific to the given tag.
    tag
    Given tag.
    """
    tag = urllib.unquote(unicode(slug)) # russian tags
    tag = get_object_or_404(Tag, name__iexact=tag)
    return list_detail.object_list(
        request,
        queryset=TaggedItem.objects.get_by_model(Photo,tag),
        extra_context={'tag': tag},
        template_name=template_name,
        **kwargs
    )


def video_detail(request, fvideo_id):
    object = Video.objects.get(id=fvideo_id)
    return direct_to_template(request, 'fgallery/video_detail.html', {'object': object} )

def video_list(request):
    object_list = Video.objects.published()
    return direct_to_template(request, 'fgallery/video_list.html', {'object_list': object_list} )
