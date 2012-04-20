from django.conf.urls import url, include, patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'kernel.views.home'),
    url(r'^clone$', 'kernel.views.clone'),
    url(r'^pull$', 'kernel.views.pull'),
)
