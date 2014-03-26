from django.conf.urls import patterns, url

from fqueryApp import views

urlpatterns = patterns('',
    url(r'^$', views.render_login, name = 'render_login'),
    url(r'^render_login/$', views.render_login, name = 'render_login'),
)