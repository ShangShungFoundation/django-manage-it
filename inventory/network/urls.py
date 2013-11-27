from django.conf.urls import patterns, url

urlpatterns = patterns('network.views',
    url(r'^connections/$', "connections", name='connections_json'),
    url(r'^$', "get", name='networks'),
)
