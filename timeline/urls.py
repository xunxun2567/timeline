from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'kernel.views.one_day'),
    url(r'^api/(?P<collector>\w+)/timeline.json', 'kernel.api.json_response'),
    # Examples:
    # url(r'^$', 'timeline.views.home', name='home'),
    # url(r'^timeline/', include('timeline.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
