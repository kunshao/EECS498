# Create your views here.
from django.shortcuts import render,render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson

from fqueryApp.models import Status, Comment, Photo, Link, Note, Video, Post, Question, QuestionOption

from fquery import settings


def render_login(request):
    print 'render_login'
    return render_to_response('home/login.html', 
        {
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
        }
    )

def home(request):
    print 'home'
    return render_to_response('home/home.html', 
        {
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
        }
    )


@csrf_exempt
def save_statuses(request):
    print 'save_statuses'
    json_data = simplejson.load(request)
    local_save_statuses(json_data)
    return HttpResponse("Finished storing statuses for user")

def local_save_statuses(status_arrary):
    print 'local_save_statuses'
    

    for json_obj in status_arrary:
        status, created = Status.objects.get_or_create(status_id = json_obj['id'])
        status.status_from_id = json_obj['from']['id']
        status.status_message = json_obj['message']
        status.status_updated_time = json_obj['updated_time']
        status.save()

@csrf_exempt
def save_photos(request):
    print 'save_pictures'
    json_data = simplejson.load(request)
    local_save_photos(json_data)
    return HttpResponse("Finished storing pictures for user")

def local_save_photos(arrary):
    print 'local_save_pictures'
    
    for json_obj in arrary:

        photo_obj, created = Photo.objects.get_or_create(photo_id = json_obj['id'])
        photo_obj.photo_from_id = json_obj['from']['id']
        photo_obj.photo_link = json_obj['link']
        if ('name' in json_obj):
            photo_obj.photo_name = json_obj['name']
        photo_obj.photo_created_time = json_obj['created_time']
        photo_obj.save()



@csrf_exempt
def save_links(request):
    print 'save_links'
    json_data = simplejson.load(request)
    local_save_links(json_data)
    return HttpResponse("Finished storing links for user")

def local_save_links(arrary):
    print 'local_save_links'
    
    for json_obj in arrary:

        link_obj, created = Link.objects.get_or_create(link_id = json_obj['id'])
        link_obj.link_created_time = json_obj['created_time']
        link_obj.link_from_id = json_obj['from']['id']
        link_obj.link_link = json_obj['link']
        if ('message' in json_obj):
            link_obj.link_message = json_obj['message']
        if ('name' in json_obj):
            link_obj.photo_name = json_obj['name']

        link_obj.save()





def index(request):
    status_list = status.objects.all()
    template = loader.get_template('status/index.html')
    context = RequestContext(request, {
            'status_list': status_list,})
    return HttpResponse(template.render(context))
