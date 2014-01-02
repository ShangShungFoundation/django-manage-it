from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from models import SLA, Document


class SLAForm(ModelForm):
    class Meta:
        model = SLA
        #fields = ['pub_date', 'headline', 'content', 'reporter']
        exclude = ("created_at", "created_by", "service", "terminated")


DocumentFormSet = inlineformset_factory(
    SLA, Document,
    max_num=2,
    exclude=("created_at", "created_by"))
