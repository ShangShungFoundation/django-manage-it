
from django import forms
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = (
            "url", "groups", "staff_group", "accounting_group",
            "admin_group", "incident_notification_group", "top_group",
            "vip_group", "purchase_notification_group")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = (
            "user_permissions", "date_joined",
            "is_superuser", "last_login")  # "groups"


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = (
            "user_permissions", "date_joined", "password"
            "is_superuser", "last_login")  # "groups"


class GroupForm(forms.ModelForm):
    """
    """

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Users'),
            is_stacked=False
        )
    )

    class Meta:
        model = Group
        exclude = ("permissions",)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super(GroupForm, self).save(commit=False)

        if commit:
            group.save()

        if group.pk:
            group.users = self.cleaned_data['users']
            self.save_m2m()
            current_users = self.instance.user_set.all()
            #we must add users this way becous we are on right side of m2m
            for usr in group.users:
                self.instance.user_set.add(usr)
            for usr in current_users:
                if usr not in group.users:
                    self.instance.user_set.remove(usr)
        return group
