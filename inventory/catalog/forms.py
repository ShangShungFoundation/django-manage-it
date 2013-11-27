from django.forms import ModelForm

from catalog.models import ItemTemplate


class ItemTemplateForm(ModelForm):
    class Meta:
        model = ItemTemplate
        #fields = ['pub_date', 'headline', 'content', 'reporter']
        exclude = ("property_number", )


