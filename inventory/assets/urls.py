from django.conf.urls import patterns, url

urlpatterns = patterns('assets.views',
    url(r'^categories/$', "categories", name='assets-categories'),
    url(r'^request/$', "new_asset_request", name='asset-request-form'),
    url(r'^request/(?P<object_id>.*)/$', "asset_request", name='asset-request'),
    url(r'^add/(?P<slug>.*)/$', "add", name='assets-add'),
    url(r'^edit/(?P<slug>.*)/$', "edit", name='assets-edit'),
    url(r'^delete/(?P<slug>.*)/$', "delete", name='assets-delete'),
    url(r'^json/(?P<slug>.*)/$', "get_json", name='get_json'),
    url(r'^(?P<slug>.*)/$', "get", name='asset_view'),
)
