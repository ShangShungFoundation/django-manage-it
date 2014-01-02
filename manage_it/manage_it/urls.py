from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

ORG_URL = "(?P<org_url>.+)/"

urlpatterns = patterns('',
    url(r'^$',
        "organizations.views.list_organizations", name='home'),
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^%sdashboard/' % ORG_URL,
        "manage_it.views.dashboard", name='dashboard'),
    url(r'^%sinventory/' % ORG_URL,
        include("catalog.urls")),
    url(r'^%sassets/' % ORG_URL,
        include("assets.urls")),
    url(r'^network/',
        include("network.urls")),
    url(r'^%sincidents/' % ORG_URL,
        include("incidents.urls")),
    url(r'^%sservices/' % ORG_URL,
        include('services.urls')),
    url(r'^%sorganization/' % ORG_URL,
        include('organizations.urls')),

    url(r'^api/', include("catalog.api_urls")),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
