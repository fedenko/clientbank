from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('cbank',),
}

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$',  'cbank.views.index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^services/$', 'cbank.views.service'),
    (r'^formservice/$', 'cbank.views.formservice'),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC}),    
)
