## Inventory Forms ##

from django import forms
from django.utils import timezone
from django.forms import CharField, Select, FileInput
from django.utils.translation import ugettext_lazy as _
from crispy_forms import layout, bootstrap
from crispy_forms.helper import FormHelper
from simple_history.utils import update_change_reason
from inventory.models import  Device
from inventory.models import ServiceContract, Service

# Device
#'title', 'make', 'model', 'purpose', 'variation', 'serial_number', 'status', 'condition', 'returnable', 'service_id',
#'model_number', 'warranty_title', 'warranty_contact', 'warranty_duration', 'warranty_id', 'warranty_terms',
#'warranty_start', 'warranty_end', 'warranty_extended', 'purchased', 'manufacturer', 'rep', 'vendor',
#'service_contract', 'type', 'status', 'classification', 'category', 'authorisation', 'resposible_party',
#'warranty_vendor', 'warranty_responsible',
    

## Abstract Forms
class CrispyDeviceCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyDeviceCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('title', wrapper_class='col-md-6'),
                        layout.Field('make', wrapper_class='col-md-6'),
                        layout.Field('model', wrapper_class='col-md-6'),
                        layout.Field('purpose', wrapper_class='col-md-6'),
                        layout.Field('variation', wrapper_class='col-md-6'),
                        layout.Field('serial_number', wrapper_class='col-md-6'),
                        layout.Field('condition'),
                        layout.Field('returnable'),
                        layout.Field('service_id', wrapper_class='col-md-6'),
                        layout.Field('model_number', wrapper_class='col-md-6'),
                        layout.Field('warranty_title', wrapper_class='col-md-6'),
                        layout.Field('warranty_contact'),
                        layout.Field('warranty_duration', wrapper_class='col-md-6'),
                        layout.Field('warranty_id', wrapper_class='col-md-6'),
                        layout.Field('warranty_terms', wrapper_class='col-md-6'),
                        layout.Field('warranty_start', wrapper_class='col-md-6'),
                        layout.Field('warranty_end', wrapper_class='col-md-6'),
                        layout.Field('warranty_extended', wrapper_class='col-md-6'),
                        layout.Field('purchased'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("manufacturer"),
                          layout.Field("type"),
                          layout.Field("status"),

                          layout.Field("classification"),
                          layout.Field("category"),
                          layout.Field("resposible_party"),
                          layout.Field("authorisation"),
                          layout.Field("warranty_vendor"),
                          layout.Field("warranty_responsible"),
                          ),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = Device
        fields = ('title', 'make', 'model', 'purpose', 'variation', 'serial_number', 'status', 'condition', 'returnable', 'service_id',
                  'model_number', 'warranty_title', 'warranty_contact', 'warranty_duration', 'warranty_id', 'warranty_terms',
                  'warranty_start', 'warranty_end', 'warranty_extended', 'purchased', 
                  'manufacturer', 'rep', 'vendor',
                  'service_contract', 'type', 'status', 'classification', 'category', 'authorisation', 'resposible_party',
                  'warranty_vendor', 'warranty_responsible')

    def save(self):
        instance = super(CrispyDeviceCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CrispyDeviceUpdateForm(forms.ModelForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def __init__(self, *args, **kwargs):
        super(CrispyDeviceUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('title', wrapper_class='col-md-6'),
                        layout.Field('make', wrapper_class='col-md-6'),
                        layout.Field('model', wrapper_class='col-md-6'),
                        layout.Field('purpose', wrapper_class='col-md-6'),
                        layout.Field('variation', wrapper_class='col-md-6'),
                        layout.Field('serial_number', wrapper_class='col-md-6'),
                        layout.Field('condition'),
                        layout.Field('returnable'),
                        layout.Field('service_id', wrapper_class='col-md-6'),
                        layout.Field('model_number', wrapper_class='col-md-6'),
                        layout.Field('warranty_title', wrapper_class='col-md-6'),
                        layout.Field('warranty_contact'),
                        layout.Field('warranty_duration', wrapper_class='col-md-6'),
                        layout.Field('warranty_id', wrapper_class='col-md-6'),
                        layout.Field('warranty_terms', wrapper_class='col-md-6'),
                        layout.Field('warranty_start', wrapper_class='col-md-6'),
                        layout.Field('warranty_end', wrapper_class='col-md-6'),
                        layout.Field('warranty_extended', wrapper_class='col-md-6'),
                        layout.Field('purchased'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("manufacturer"),
                          layout.Field("type"),
                          layout.Field("status"),

                          layout.Field("classification"),
                          layout.Field("category"),
                          layout.Field("resposible_party"),
                          layout.Field("authorisation"),
                          layout.Field("warranty_vendor"),
                          layout.Field("warranty_responsible"),
                          layout.Field('change_reason', wrapper_class='col-md-6'),
                          ),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = Device
        fields = ('title', 'make', 'model', 'purpose', 'variation', 'serial_number', 'status', 'condition', 'returnable', 'service_id',
                  'model_number', 'warranty_title', 'warranty_contact', 'warranty_duration', 'warranty_id', 'warranty_terms',
                  'warranty_start', 'warranty_end', 'warranty_extended', 'purchased', 
                  'manufacturer', 'rep', 'vendor',
                  'service_contract', 'type', 'status', 'classification', 'category', 'authorisation', 'resposible_party',
                  'warranty_vendor', 'warranty_responsible')

    def save(self):
        instance = super(CrispyDeviceUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class DeviceCreateForm(forms.ModelForm):
    
    class Meta:
        model = Device
        fields = ('title', 'make', 'model', 'purpose', 'variation', 'serial_number', 'status', 'condition', 'returnable', 'service_id',
                  'model_number', 'warranty_title', 'warranty_contact', 'warranty_duration', 'warranty_id', 'warranty_terms',
                  'warranty_start', 'warranty_end', 'warranty_extended', 'purchased', 'manufacturer', 'rep', 'vendor',
                  'service_contract', 'type', 'status', 'classification', 'category', 'authorisation', 'resposible_party',
                  'warranty_vendor', 'warranty_responsible')
    
    def save(self):
        instance = super(DeviceForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class DeviceUpdateForm(forms.ModelForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    class Meta:
        model = Device
        fields = ('title', 'make', 'model', 'purpose', 'variation', 'serial_number', 'status', 'condition', 'returnable', 'service_id',
                  'model_number', 'warranty_title', 'warranty_contact', 'warranty_duration', 'warranty_id', 'warranty_terms',
                  'warranty_start', 'warranty_end', 'warranty_extended', 'purchased', 'manufacturer', 'rep', 'vendor',
                  'service_contract', 'type', 'status', 'classification', 'category', 'authorisation', 'resposible_party',
                  'warranty_vendor', 'warranty_responsible')

    def save(self):
        instance = super(DeviceUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CommentCreateForm(forms.ModelForm):
    '''Form for updating a comment.
    '''
    text = forms.CharField(label='Comment: ', widget=forms.Textarea,
                             max_length=500, required=True)
    class Meta:
        fields = ('text',)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-edit_comment_form'
        self.helper.form_class = "form-widget"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                "Edit comment",
                "text",
            ),
            ButtonHolder(
                Submit('submit', "Submit")
            )
        )
        return super(CommentUpdateForm, self).__init__(*args, **kwargs)


class CommentUpdateForm(forms.ModelForm):
    '''Form for updating a comment.
    '''
    text = forms.CharField(label='Comment: ', widget=forms.Textarea,
                             max_length=500, required=True)
    class Meta:
        fields = ('text',)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-edit_comment_form'
        self.helper.form_class = "form-widget"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                "Edit comment",
                "text",
            ),
            ButtonHolder(
                Submit('submit', "Submit")
            )
        )
        return super(CommentUpdateForm, self).__init__(*args, **kwargs)


## Main Forms
class ServiceContractForm(forms.ModelForm):
    class Meta:
        model = ServiceContract
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
