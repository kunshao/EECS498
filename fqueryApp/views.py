# Create your views here.
from django.shortcuts import render,render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse

from fqueryApp.models import status
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

def index(request):
    status_list = status.objects.all()
    template = loader.get_template('status/index.html')
    context = RequestContext(request, {
            'status_list': status_list,})
    return HttpResponse(template.render(context))