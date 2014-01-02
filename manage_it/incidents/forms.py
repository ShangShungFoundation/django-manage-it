from django.forms import ModelForm
from django import forms

from models import Incident, IncidentFollowup


class NewIncidentForm(ModelForm):
    class Meta:
        model = Incident
        exclude = (
            "organization", "submited_at", "submited_by",
            "status", "assigned_to", "priority", "daedline")

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

    def save(self, commit=True):
        #import ipdb; ipdb.set_trace()
        instance = super(IncidentFollowupFormAdmin, self).save(commit=False)
        instance.save()
        return super(IncidentFollowupFormAdmin, self).save()


class IncidentFollowupForm(ModelForm):
    incident = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = IncidentFollowup
        exclude = ("created_at", "created_by", "incident", "status_change",)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.save()
        return super(IncidentFollowupForm, self).form_valid(form)
