"""
Case Forms.
"""

from django import forms
from case.models import Case, CaseNote, CaseTask, CaseEvidence
#, CaseTask, CaseNote
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, CharField, Textarea, Select, FileInput
from django.utils.text import slugify
import itertools
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from simple_history.utils import update_change_reason

#fields = ['brief',
#           'type', 'status', 'classification', 'priority', 'category',
#           'authorisation', 'assigned_to', 'manager', 'assigned_by',
#           'description', 'private']

# Case
class CrispyCaseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyCaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('title', wrapper_class='col-md-6'),
                        layout.Field('reference', wrapper_class='col-md-6'),
                        layout.Field('background', wrapper_class='col-md-9'),
                        layout.Field('purpose', wrapper_class='col-md-3'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Main data"),
                          layout.Field("location", css_class="input-block-level"),
                          layout.Field("brief", css_class="input-block-level"),
                          layout.Field("description", css_class="input-blocklevel", rows="3"),
                          layout.Field("private"),
                          layout.Field("type"),
                          layout.Div(bootstrap.PrependedText("status", "", css_class="input-block-level"), css_id="contact_info",),
                          layout.Div(bootstrap.PrependedText("classification", "", css_class="input-block-level"), css_id="contact_info",),
                          layout.Div(bootstrap.PrependedText("priority", "", css_class="input-block-level"), css_id="contact_info",),
                          layout.Div(bootstrap.PrependedText("category", "", css_class="input-block-level"), css_id="contact_info",),
                          layout.Div(bootstrap.PrependedText("authorisation", "", css_class="input-block-level"), css_id="contact_info",),),

            layout.Fieldset(_("Image"),
                          layout.Field("image_upload", css_class="input-block-level"),
                          layout.HTML(u"""{% load i18n %}
                            <p class="help-block">
                                {% trans "Available formats are JPG, GIF, and PNG. Minimal size is 800 × 800 px." %}
                            </p>"""),
                          title=_("Image upload"), css_id="image_fieldset",),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("assigned_by"),
                          layout.Field("assigned_to"), 
                          layout.Field("managed_by"),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = Case
        fields = ['title', 'reference', 'background', 'purpose', 'location', 'brief',
                  'image_upload',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'managed_by', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CrispyCaseForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Case.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Case Creation')
        return instance


class CaseCreateForm(forms.ModelForm):

    title = CharField(max_length=200, required=False,)
    reference = CharField(max_length=200, required=False,)
    background = CharField(required=False,)
    location = CharField(max_length=200, required=False,)
    description = CharField(required=False,)
    brief = CharField(required=False,)
   
    class Meta:
        model = Case
        fields = ['title', 'reference', 'background', 'purpose', 'location', 'brief',
                  'image_upload', 
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'managed_by', 'assigned_by',
                  'description', 'private']
        
        labels = {
            'type': _('Case Type'),
            'title':_('Title'),
            'reference':_('Reference'),
            'background':_('Background'),
            'location':_('Location'),
            'description':_('Description'),
            'brief':_('Brief'),
        }
        error_messages = {
            'case': {'max_length': _("The Case Type is Invalid"),},
        }
        help_texts = {
            'title': _('Some useful help text.'),
        }
        widgets = {
            #'authorisation': Select(attrs={'class': 'form-control'}),
            #'priority': Select(attrs={'class': 'form-control'}),
            #'classification': Select(attrs={'class': 'form-control'}),
            #'status': Select(attrs={'class': 'form-control'}),
            #'type': Select(attrs={'class': 'form-control'}),
            #'assigned_by': Select(attrs={'class': 'form-control'}),
            #'assigned_to': Select(attrs={'class': 'form-control'}),
            #'manager': Select(attrs={'class': 'form-control'}),
            #'title': CharField(attrs={'max_length': 200, 'required': False}),
        }

    def save(self):
        instance = super(CaseCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Case.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Case Creation')
        return instance


class CaseUpdateForm(forms.ModelForm):

    change_reason = CharField(required=False, label='Reason For Change',)
    title = CharField(max_length=200, required=False,)
    reference = CharField(max_length=200, required=False,)
    background = CharField(required=False,)
    location = CharField(max_length=200, required=False,)
    description = CharField(required=False,)
    brief = CharField(required=False,)
   
    class Meta:
        model = Case
        fields = ['title', 'reference', 'background', 'purpose', 'location', 'brief',
                  'image_upload',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'managed_by', 'assigned_by',
                  'description', 'private']
        labels = {
            'type': _('Case Type'),
            'title':_('Title'),
            'reference':_('Reference'),
            'background':_('Background'),
            'location':_('Location'),
            'description':_('Description'),
            'brief':_('Brief'),
        }
        error_messages = {
            'case': {'max_length': _("The Case Type is Invalid"),},
        }
        help_texts = {
            'title': _('Some useful help text.'),
        }
        widgets = {
            'authorisation': Select(attrs={'class': 'form-control'}),
            'priority': Select(attrs={'class': 'form-control'}),
            'classification': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'assigned_by': Select(attrs={'class': 'form-control'}),
            'assigned_to': Select(attrs={'class': 'form-control'}),
            'manager': Select(attrs={'class': 'form-control'}),
            'image_upload': FileInput(attrs={'class': 'form-control'}),
            #'title': CharField(attrs={'max_length': 200, 'required': False}),
        }

    def save(self):
        instance = super(CaseUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Case.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, 'Initial Case Creation')
        return instance

    
# Case Note
class CrispyCaseNoteCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyCaseNoteCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('title', wrapper_class='col-md-6'),
                        layout.Field('brief', wrapper_class='col-md-6'),
                        layout.Field('type', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Main data"),
                          layout.Field("description"),
                          layout.Field("status", css_class="input-blocklevel", rows="3"),
                          layout.Field("classification"),
                          layout.Field("priority"),),

            layout.Fieldset(_("Image"),
                          layout.Field("image_upload", css_class="input-block-level"),
                          layout.HTML(u"""{% load i18n %}
                            <p class="help-block">
                                {% trans "Available formats are JPG, GIF, and PNG. Minimal size is 800 × 800 px." %}
                            </p>"""),
                          title=_("Image upload"), css_id="image_fieldset",),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("category"),
                          layout.Field("authorisation"),
                          layout.Field("assigned_to"),
                          layout.Field("manager"),
                          layout.Field("assigned_by"),
                          layout.Field("assigned_to"),
                          layout.Field("private"),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = CaseNote
        fields = ['title', 'image_upload', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CrispyCaseNoteCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseNote.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Note Creation')
        return instance


class CaseNoteCreateForm(forms.ModelForm):
        
    #def __init__(self, casepk=None, *args, **kwargs):
    #    super(CaseNoteCreateForm,self).__init__(*args,**kwargs)
    #    self.case = Case.objects.get(id=kwargs['casepk'])
    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CaseNote
        fields = ['title', 'image_upload', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CaseNoteCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseNote.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        #changereason = self.cleaned_data['change_reason']
        instance.save()
        #update_change_reason(instance, changereason)
        return instance


class CaseNoteUpdateForm(forms.ModelForm):
        
    title = CharField(max_length=200, required=False, label='Title',)
    change_reason = CharField(required=False, label='Reason For Change',)
    
    class Meta:
        model = CaseNote
        fields = ['title', 'image_upload', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CaseNoteUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseNote.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


# Case Task
class CrispyCaseTaskCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyCaseTaskCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('title', wrapper_class='col-md-6'),
                        layout.Field('background', wrapper_class='col-md-6'),
                        layout.Field('location', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Main data"),
                          layout.Field("brief", css_class="input-blocklevel", rows="3"),
                          layout.Field("type"),
                          layout.Field("status"),),

            layout.Fieldset(_("Image"),
                          layout.Field("image_upload", css_class="input-block-level"),
                          layout.HTML(u"""{% load i18n %}
                            <p class="help-block">
                                {% trans "Available formats are JPG, GIF, and PNG. Minimal size is 800 × 800 px." %}
                            </p>"""),
                          title=_("Image upload"), css_id="image_fieldset",),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("classification"),
                          layout.Field("priority"),
                          layout.Field("category"),
                          layout.Field("authorisation"),
                          layout.Field("assigned_to"),
                          layout.Field("manager"),
                          layout.Field("assigned_by"),
                          layout.Field("description"),
                          layout.Field("private"),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = CaseTask
        fields = ['title', 'background', 'location', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CrispyCaseTaskCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseTask.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Task Creation')
        return instance


class CaseTaskCreateForm(forms.ModelForm):
        
    #def __init__(self, casepk=None, *args, **kwargs):
    #    super(CaseTaskCreateForm,self).__init__(*args,**kwargs)
    #    self.case = Case.objects.get(id=kwargs['casepk'])
    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CaseTask
        fields = ['title', 'background', 'location', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CaseTaskCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseTask.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        #changereason = self.cleaned_data['change_reason']
        instance.save()
        #update_change_reason(instance, changereason)
        return instance


class CaseTaskUpdateForm(forms.ModelForm):

    title = CharField(max_length=200, required=False, label='Title',)
    change_reason = CharField(required=False, label='Reason For Change',)
    
    class Meta:
        model = CaseTask
        fields = ['title', 'background', 'location', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CaseTaskUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseTask.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


# Case Evidence
class CrispyCaseEvidenceCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyCaseEvidenceCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('title', wrapper_class='col-md-6'),
                        layout.Field('reference', wrapper_class='col-md-6'),
                        layout.Field('comment', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('bag_number', wrapper_class='col-md-6'),
                        layout.Field('location', wrapper_class='col-md-6'),
                        layout.Field('uri', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('current_status', wrapper_class='col-md-6'),
                        layout.Field('qr_code_text', wrapper_class='col-md-6'),
                        layout.Field('qr_code', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('bag_number', wrapper_class='col-md-6'),
                        layout.Field('location', wrapper_class='col-md-6'),
                        layout.Field('uri', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('retention_date', wrapper_class='col-md-6'),
                        layout.Field('brief', wrapper_class='col-md-9'),
                        layout.Field('custodian', wrapper_class='col-md-9'),
                        layout.Field('chain_of_custody', wrapper_class='col-md-9'),
                        layout.Field('type', wrapper_class='col-md-9'),
                        layout.Field('status', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('classification', wrapper_class='col-md-6'),
                        layout.Field('priority', wrapper_class='col-md-6'),
                        layout.Field('category', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Main data"),
                          layout.Field("authorisation", css_class="input-blocklevel", rows="3"),
                          layout.Field("assigned_to"),
                          layout.Field("assigned_by"),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = CaseEvidence
        fields = ['title', 'reference', 'comment', 'bag_number', 'location',
                  'uri', 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
                  'retention_date', 'brief', 'custodian', 'chain_of_custody',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CrispyCaseEvidenceCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvidence.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Evidence Creation')
        return instance


class CaseEvidenceCreateForm(forms.ModelForm):
        
    #def __init__(self, casepk=None, *args, **kwargs):
    #    super(CaseEvidenceCreateForm,self).__init__(*args,**kwargs)
    #    self.case = Case.objects.get(id=kwargs['casepk'])
    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CaseEvidence
        fields = ['title', 'reference', 'comment', 'bag_number', 'location',
                  'uri', 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
                  'retention_date', 'brief', 'custodian', 'chain_of_custody',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CaseEvidenceCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvidence.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        #changereason = self.cleaned_data['change_reason']
        instance.save()
        #update_change_reason(instance, changereason)
        return instance


class CaseEvidenceUpdateForm(forms.ModelForm):

    title = CharField(max_length=200, required=False, label='Title',)
    change_reason = CharField(required=False, label='Reason For Change',)
    
    class Meta:
        model = CaseEvidence
        fields = ['title', 'reference', 'comment', 'bag_number', 'location',
                  'uri', 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
                  'retention_date', 'brief', 'custodian', 'chain_of_custody',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'assigned_by',
                  'description', 'private']

    def save(self):
        instance = super(CaseEvidenceUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvidence.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance