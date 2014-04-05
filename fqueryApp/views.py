# Create your views here.
from django.shortcuts import render,render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson

from fqueryApp.models import Status, Comment
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
    

    for status_json_obj in status_arrary:
        print status_json_obj
        print status_json_obj['id']
        print status_json_obj['from']['id']
        print status_json_obj['message']
        print status_json_obj['updated_time']
        status, created = Status.objects.get_or_create(status_id = status_json_obj['id'])
        status.status_from_id = status_json_obj['from']['id']
        status.status_message = status_json_obj['message']
        status.status_updated_time = status_json_obj['updated_time']
        status.save()




def index(request):
    status_list = status.objects.all()
    template = loader.get_template('status/index.html')
    context = RequestContext(request, {
            'status_list': status_list,})
    return HttpResponse(template.render(context))
