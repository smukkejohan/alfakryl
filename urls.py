from django.conf.urls.defaults import *

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^alfakryl/', include('alfakryl.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^$',       'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    
    (r'^accounts/', include('registration.urls')),
)

if settings.DEVELOPMENT_MODE:
    urlpatterns += patterns('django.views',
        url(r'%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'static.serve', {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
    )
