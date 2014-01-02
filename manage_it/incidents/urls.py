from django.conf.urls import patterns, url

urlpatterns = patterns('incidents.views',
    url(r'^new/$', "new", name='incident_new'),
    url(r'^followup/(?P<object_id>.*)/$',
        "new_followup", name='incident_followup'),
    url(r'^(?P<object_id>.*)/$', "get", name='incident'),
    url(r'^$', "list", name='incidents'),
)
