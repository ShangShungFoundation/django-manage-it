from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'inventory.views.home', name='home'),
    # url(r'^inventory/', include('inventory.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', "inventory.views.dashboard"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', include("catalog.urls")),
    url(r'^assets/', include("assets.urls")),
    url(r'^network/', include("network.urls")),
    url(r'^incidents/', include("incidents.urls")),
    url(r'^api/', include("catalog.api_urls")),
    url(r'^accounts/', include('allauth.urls')),
    
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

 

