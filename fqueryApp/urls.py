from django.conf.urls import patterns, url
from fqueryApp import views

urlpatterns = patterns('',
    url(r'^home/$', views.home, name = 'home'),
    url(r'^redirect_home/$', views.home, name = 'redirect_home'),
    url(r'^$', views.render_login, name = 'render_login'),

    url(r'^render_login/$', views.render_login, name = 'render_login'),

    # url to save all statuses by the user. Shouldn't be called by user.
    url(r'^save_statuses/$', views.save_statuses, name = 'save_statuses'),    

    # url to save all pictures of the user. Shouldn't be called by user.
    url(r'^save_photos/$', views.save_photos, name = 'save_photos'),    
    
    # url(r'^render_login/$', views.render_login, name = 'render_login'),
    url(r'^search/$', views.index, name='search')
    
)
