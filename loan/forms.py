## Loan Forms ##

from django import forms
from django.forms import CharField
from django.utils.translation import ugettext_lazy as _
from crispy_forms import layout, bootstrap
from crispy_forms.helper import FormHelper
from simple_history.utils import update_change_reason
from loan.models import  Loan


''' Loan 
'reason', 'booked_from', 'booked_until', 'original_condition', 'returned_condition', 'returned', 'case', 'device', 'loaned_to',
'loaned_by', 'description', 'private', 'status', 'taken'
'''


## Abstract Forms
class LoanForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('reason', wrapper_class='col-md-6'),
                        layout.Field('change_reason', wrapper_class='col-md-6'),
                        layout.Field('booked_from', wrapper_class='col-md-6'),
                        layout.Field('booked_until', wrapper_class='col-md-6'),
                        layout.Field('original_condition', wrapper_class='col-md-6'),
                        layout.Field('returned', wrapper_class='col-md-6'),
                        layout.Field('case', wrapper_class='col-md-6'),
                        layout.Field('device'),
                        layout.Field('loaned_to'),
                        layout.Field('loaned_by', wrapper_class='col-md-6'),
                        layout.Field('description', wrapper_class='col-md-6'),
                        layout.Field('private', wrapper_class='col-md-6'),
                        )),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = Loan
        fields = ('reason', 'booked_from', 'booked_until', 'original_condition', 'returned', 'case', 'device', 'loaned_to',
                  'loaned_by', 'description', 'private')


class __LoanForm(forms.ModelForm):
    
    class Meta:
        model = Loan
        fields = ('reason', 'booked_from', 'booked_until', 'original_condition', 'returned', 'case', 'device', 'loaned_to',
                  'loaned_by', 'description', 'private')


## Loan Forms
class CrispyLoanCreateForm(LoanForm):
    
    def save(self):
        instance = super(CrispyLoanCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CrispyLoanUpdateForm(LoanForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)
    
    def save(self):
        instance = super(CrispyLoanUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class LoanCreateForm(__LoanForm):

    def save(self):
        instance = super(LoanForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class LoanUpdateForm(__LoanForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(LoanUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


## Loan With Case Forms
class CrispyLoanWithCaseCreateForm(CrispyLoanCreateForm):

    class Meta:
        model = Loan
        fields = ('booked_from', 'device', 'loaned_to', 'reason', 'booked_until', 'description', 'private')


class CrispyLoanWithCaseUpdateForm(CrispyLoanUpdateForm):

    class Meta:
        model = Loan
        fields = ('booked_from', 'device', 'loaned_to', 'reason', 'booked_until', 'description', 'private')


## Loan With Device Forms
class CrispyLoanWithDeviceCreateForm(CrispyLoanCreateForm):
    
    class Meta:
        model = Loan
        fields = ('booked_from', 'case', 'loaned_to', 'reason', 'booked_until', 'description', 'private')


class CrispyLoanWithDeviceUpdateForm(CrispyLoanUpdateForm):

    class Meta:
        model = Loan
        fields = ('booked_from', 'case', 'loaned_to', 'reason', 'booked_until', 'description', 'private')


## Loan With Both Forms
class CrispyLoanWithBothCreateForm(CrispyLoanCreateForm):
    
    class Meta:
        model = Loan
        fields = ('booked_from', 'loaned_to', 'reason', 'status', 
                  'booked_until', 'description', 'private')


class CrispyLoanWithBothUpdateForm(CrispyLoanUpdateForm):

    class Meta:
        model = Loan
        fields = ('booked_from', 'loaned_to', 'reason', 'booked_until', 'description', 'private')
