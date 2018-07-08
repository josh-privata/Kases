"""
Entity Forms
"""
from django import forms
from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _
from django.forms import modelformset_factory as inlineformset_factory

from entity import models


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ('name', 'nickname', 'about')


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = '__all__'


class PersonCreateForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ('first_name', 'last_name', 'title', 'company', 'about')


class PersonUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ('first_name', 'last_name', 'title', 'company')


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = '__all__'
        widgets = {
            'people': widgets.FilteredSelectMultiple(
                _("People"), is_stacked=False),
            'companies': widgets.FilteredSelectMultiple(
                _("Companies"), is_stacked=False),
        }


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ('name', 'about')


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Group
        exclude = ('slug',)


PhoneNumberFormSet = inlineformset_factory(models.PhoneNumber, fields='__all__')
EmailAddressFormSet = inlineformset_factory(models.EmailAddress, fields='__all__')
InstantMessengerFormSet = inlineformset_factory(models.InstantMessenger, fields='__all__')
WebSiteFormSet = inlineformset_factory(models.WebSite, fields='__all__')
StreetAddressFormSet = inlineformset_factory(models.StreetAddress, fields='__all__')
SpecialDateFormSet = inlineformset_factory(models.SpecialDate, fields='__all__')