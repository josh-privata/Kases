## Loan Forms ##

from django import forms
from django.utils import timezone
from django.forms import CharField, Select, FileInput
from django.utils.translation import ugettext_lazy as _
from crispy_forms import layout, bootstrap
from crispy_forms.helper import FormHelper
from simple_history.utils import update_change_reason
from loan.models import  Loan

# Loan 
#'reason', 'booked_from', 'booked_until', 'condition', 'returned', 'case', 'device', 'loaned_to',
#'loaned_by', 'description', 'private'

## Abstract Forms
class CrispyLoanCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyLoanCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('reason', wrapper_class='col-md-6'),
                        layout.Field('booked_from', wrapper_class='col-md-6'),
                        layout.Field('booked_until', wrapper_class='col-md-6'),
                        layout.Field('condition', wrapper_class='col-md-6'),
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
        fields = ('reason', 'booked_from', 'booked_until', 'condition', 'returned', 'case', 'device', 'loaned_to',
                  'loaned_by', 'description', 'private')

    def save(self):
        instance = super(CrispyLoanCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CrispyLoanUpdateForm(forms.ModelForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def __init__(self, *args, **kwargs):
        super(CrispyLoanUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('reason', wrapper_class='col-md-6'),
                        layout.Field('booked_from', wrapper_class='col-md-6'),
                        layout.Field('booked_until', wrapper_class='col-md-6'),
                        layout.Field('condition', wrapper_class='col-md-6'),
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
        fields = ('reason', 'booked_from', 'booked_until', 'condition', 'returned', 'case', 'device', 'loaned_to',
                  'loaned_by', 'description', 'private')

    def save(self):
        instance = super(CrispyLoanUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class LoanCreateForm(forms.ModelForm):
    
    class Meta:
        model = Loan
        fields = ('reason', 'booked_from', 'booked_until', 'condition', 'returned', 'case', 'device', 'loaned_to',
                  'loaned_by', 'description', 'private')
    
    def save(self):
        instance = super(LoanForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class LoanUpdateForm(forms.ModelForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    class Meta:
        model = Loan
        fields = ('reason', 'booked_from', 'booked_until', 'condition', 'returned', 'case', 'device', 'loaned_to',
                  'loaned_by', 'description', 'private')

    def save(self):
        instance = super(LoanUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


#class CommentCreateForm(forms.ModelForm):
#    '''Form for updating a comment.
#    '''
#    text = forms.CharField(label='Comment: ', widget=forms.Textarea,
#                             max_length=500, required=True)
#    class Meta:
#        fields = ('text',)
    
#    def __init__(self, *args, **kwargs):
#        self.helper = FormHelper()
#        self.helper.form_id = 'id-edit_comment_form'
#        self.helper.form_class = "form-widget"
#        self.helper.form_method = 'post'
#        self.helper.layout = Layout(
#            Fieldset(
#                "Edit comment",
#                "text",
#            ),
#            ButtonHolder(
#                Submit('submit', "Submit")
#            )
#        )
#        return super(CommentUpdateForm, self).__init__(*args, **kwargs)


#class CommentUpdateForm(forms.ModelForm):
#    '''Form for updating a comment.
#    '''
#    text = forms.CharField(label='Comment: ', widget=forms.Textarea,
#                             max_length=500, required=True)
#    class Meta:
#        fields = ('text',)
    
#    def __init__(self, *args, **kwargs):
#        self.helper = FormHelper()
#        self.helper.form_id = 'id-edit_comment_form'
#        self.helper.form_class = "form-widget"
#        self.helper.form_method = 'post'
#        self.helper.layout = Layout(
#            Fieldset(
#                "Edit comment",
#                "text",
#            ),
#            ButtonHolder(
#                Submit('submit', "Submit")
#            )
#        )
#        return super(CommentUpdateForm, self).__init__(*args, **kwargs)


## Main Forms
