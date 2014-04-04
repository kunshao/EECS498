from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fquery.views.home', name='home'),
    # url(r'^fquery/', include('fquery.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'fqueryApp.views.home', name='home'),
    url(r'^home/', include('fqueryApp.urls', namespace = 'fqueryApp')),
    url(r'^fqueryApp/', include('fqueryApp.urls')),
)
