from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin


urlpatterns = patterns('kernel.views',
    url(r'^$', 'one_day'),
    url(r'^(?P<collector_name>\w+)/$','view_today'),
    url(r'^(?P<collector_name>\w+)/(?P<time_filter>\d*)/$','view_someday'),
    
   

)
