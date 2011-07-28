from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$',  'cbank.views.index'),
    (r'^accounts/login/$',  'cbank.views.login'),
    (r'^services/$', 'cbank.views.service'),
    (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'cbank/media/output'}),    
)
