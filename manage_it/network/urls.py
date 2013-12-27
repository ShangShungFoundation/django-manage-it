from django.conf.urls import patterns, url

urlpatterns = patterns('network.views',
    url(r'^connections/$', "connections", name='connections_json'),
    url(r'^scan/(?P<network_id>\d+)/$', "scan_network", name='scan_network'),
    url(r'^$', "get", name='networks'),
)
