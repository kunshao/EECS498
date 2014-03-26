# Create your views here.
from django.shortcuts import render_to_response
from django.template import loader
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
