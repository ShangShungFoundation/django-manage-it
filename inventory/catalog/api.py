# from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from assets.models import Item
from catalog.models import ItemTemplate, Location


class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        resource_name = "locations"


class TemplateResource(ModelResource):
    #item = fields.ToOneField("ItemResource", 'item')

    class Meta:
        queryset = ItemTemplate.objects.all()
        resource_name = "item_template"

  
class ItemResource(ModelResource):
    item_template = fields.ForeignKey(TemplateResource, 'item_template', 
null=True)
    locations = fields.ForeignKey(TemplateResource, 'location', 
null=True)
    
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'items'
        #authorization= Authorization()
        filtering = {
            'item_template': ALL,
            'users': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        
