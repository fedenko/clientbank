from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$',  'cbank.views.index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^services/$', 'cbank.views.service'),
    (r'^formservice/$', 'cbank.views.processor'),
    (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'cbank/media/output'}),    
)
