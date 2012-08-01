import os.path as path

from django.conf.urls import patterns, include, url
from settings import TEMPLATE_DIRS
import settings

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^trello$', 'theapp.views.home', name='home'),
    url(r'^feed/(.+)$', 'theapp.views.feed', name='feed'),
    
    
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),


    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    #Some stuff to make runserver a real server, although in production it should be apache who serves this:
    (r'/?css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': path.join(TEMPLATE_DIRS, "css")}),
    
    (r'/?img/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': path.join(TEMPLATE_DIRS, "img")}),
    
    (r'/?js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': path.join(TEMPLATE_DIRS, "js")}),
    
    (r'/?less/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': path.join(TEMPLATE_DIRS, "less")}),
    
    
)
