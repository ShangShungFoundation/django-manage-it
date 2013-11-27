from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from assets.models import Item, Resource, AssetRequest
from catalog.models import ItemTemplate

class ItemForm(ModelForm):
    class Meta:
        model = Item
        #fields = ['pub_date', 'headline', 'content', 'reporter']
        exclude = ("property_number", "item_class", "created")

ItemSearchFormSet = inlineformset_factory(ItemTemplate, Item,  extra=1,
    fields=["property_number", "serial_number", "location", "item_class", "owner", "active", "state", "users"])

UsersFormSet = inlineformset_factory(ItemTemplate, Item,  extra=1)

ResourcesSet = inlineformset_factory(Item, Resource, extra=1)

class ItemSearchForm(ModelForm):
    class Meta:
        model = Item
        #fields = ['pub_date', 'headline', 'content', 'reporter']
        exclude = ("property_number", "configuration")
        

class AssetRequestForm(ModelForm):
    class Meta:
        model = AssetRequest
        #fields = ['pub_date', 'headline', 'content', 'reporter']
        exclude = ("new_item", "created_at", "created_by", "status")
