from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('services.views',
    url(r'^(?P<service_id>\d*)/sla/new/$',
        "add_sla", name='add_sla'),
    url(r'^(?P<service_id>\d+)/sla/new/(?P<data_form_id>\d+)/$',
        "sla_detail_form", name='sla_detail_form'),
    url(r'^(?P<service_id>\d+)/sla/edit/(?P<sla_id>\d+)/$',
        "edit_sla", name='edit_sla'),
    url(r'^(?P<service_id>\d+)/sla/(?P<object_id>\d+)/$',
        "sla_view", name='sla_view'),
    url(r'^(?P<object_id>.+)/$',
        "view_service", name='view_service'),
    url(r'^$',
        "list_services", name='list_services'),
)
