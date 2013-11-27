from django.conf.urls import patterns, include
from tastypie.api import Api

from api import ItemResource

v1_api = Api(api_name='v1')
v1_api.register(ItemResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)