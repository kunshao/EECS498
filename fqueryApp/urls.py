from django.conf.urls import patterns, url
from fqueryApp import views

urlpatterns = patterns('',
    url(r'^home/$', views.home, name = 'home'),
    url(r'^redirect_home/$', views.home, name = 'redirect_home'),
    url(r'^$', views.render_login, name = 'render_login'),

    url(r'^render_login/$', views.render_login, name = 'render_login'),
    
    # url(r'^render_login/$', views.render_login, name = 'render_login'),
    
)