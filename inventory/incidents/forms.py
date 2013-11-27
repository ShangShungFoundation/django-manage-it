from django.forms import ModelForm
from django import forms

from models import Incident, IncidentFolowup


class NewIncidentForm(ModelForm):
    class Meta:
        model = Incident
        exclude = ("created", "created_by", "status", "priority",)
        
    def form_valid(self, form):
        object = form.save(commit=False)
        
        object.created_by = self.request.user
        object.save()
        return super(NewIncidentForm, self).form_valid(form)


class IncidentFollowupFormAdmin(ModelForm):
    observations = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Incident
        fields = ("impact", "urgency", "status", "affected_devices",)
        
    def savessss(self, commit=True):
        import ipdb; ipdb.set_trace()
        instance = super(IncidentFollowupFormAdmin, self).save(commit=False)
        instance.save()
        
        
        
        return super(NewIncidentForm, self).save(*args, **kwargs)


class IncidentFollowupForm(ModelForm):
    incident = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = IncidentFolowup
        exclude = ("created_at", "created_by", "incident", "status_change",)
        
    def form_valid(self, form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.save()
        return super(NewIncidentFollowupForm, self).form_valid(form)