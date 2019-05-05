"""
Evidence Forms.
"""


from django import forms
from evidence.models import Evidence
#, EvidenceNote, EvidenceTask
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, CharField, Textarea, Select, FileInput
from django.utils.text import slugify
import itertools
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from simple_history.utils import update_change_reason


##'title', 'reference','comment', 'bag_number', 'location', 'uri', 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent', 'slug', 'type', 'status', 'classification', 'priority', 'authorisation', 'category', 'chain_of_custody', 'assigned_to', 'custodian', 'assigned_by'


##class EvidenceForm(forms.ModelForm):

##    class Meta:
##        model = Evidence
##        fields = ['title', 'reference','comment', 'bag_number', 'location', 'uri',
##                 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
##                'slug', 'type', 'status', 'classification', 'priority', 'authorisation',
##               'category', 'chain_of_custody', 'assigned_to', 'custodian', 'assigned_by']


#class CrispyEvidenceForm(forms.ModelForm):
    
#    def __init__(self, *args, **kwargs):
#        super(CrispyEvidenceForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_action = ""
#        self.helper.form_method = "POST"
#        self.helper.form_class = 'form-horizontal'
#        self.helper.label_class = 'col-lg-2'
#        self.helper.field_class = 'col-lg-8'
#        self.helper.layout = layout.Layout(
            
#            layout.Div(layout.Fieldset(_("Main data"),
#                        layout.Field('title', wrapper_class='col-md-6'),
#                        layout.Field('type', wrapper_class='col-md-6'),
#                        layout.Field('status', wrapper_class='col-md-9'),
#                        layout.Field('comment', wrapper_class='col-md-3'),
#                        #css_class='form-row'
#                        )),

#            layout.Fieldset(_("Main data"),
#                          layout.Field("classification"),),

#            layout.Fieldset(_("Authorisation"), 
#                          layout.Field("authorisation"),
#                          layout.Field("assigned_to"), 
#                          layout.Field("assigned_by"), 
#                          layout.Div(bootstrap.PrependedText("reference", "", css_class="input-block-level", placeholder="contact@example.com"), css_id="contact_info",),),

#            layout.Fieldset(_("Main data"),
#                          bootstrap.TabHolder(
#                            bootstrap.Tab('First Tab', layout.Field('location', wrapper_class='col-md-6')),
#                            bootstrap.Tab('Second Tab',layout.Field('description', wrapper_class='col-md-6')),
#                      ),),

#            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

#    class Meta:
#        model = Evidence
#        fields = ['title', 'reference','comment', 'bag_number', 'location', 'uri',
#                 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
#                'slug', 'type', 'status', 'classification', 'priority', 'authorisation',
#               'category', 'chain_of_custody', 'assigned_to', 'custodian', 'assigned_by']

#    def save(self):
#        instance = super(CrispyEvidenceForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not Evidence.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        instance.save()
#        update_change_reason(instance, 'Initial Evidence Creation')
#        return instance


#class EvidenceCreateForm(forms.ModelForm):

#    title = CharField(max_length=200, required=False,)
#    reference = CharField(max_length=200, required=False,)
#    description = CharField(required=False,)
   
#    class Meta:
#        model = Evidence
#        fields = ['title', 'reference','comment', 'bag_number', 'location', 'uri',
#                 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
#                'slug', 'type', 'status', 'classification', 'priority', 'authorisation',
#               'category', 'chain_of_custody', 'assigned_to', 'custodian', 'assigned_by']
#        labels = {
#            'type': _('Evidence Type'),
#            'title':_('Title'),
#            'reference':_('Reference'),
#            'location':_('Location'),
#            'description':_('Description'),
#        }
#        error_messages = {
#            'evidence': {'max_length': _("The Evidence Type is Invalid"),},
#        }
#        help_texts = {
#            'title': _('Some useful help text.'),
#        }
#        widgets = {
#            #'authorisation': Select(attrs={'class': 'form-control'}),
#            #'priority': Select(attrs={'class': 'form-control'}),
#            #'classification': Select(attrs={'class': 'form-control'}),
#            #'status': Select(attrs={'class': 'form-control'}),
#            #'type': Select(attrs={'class': 'form-control'}),
#            #'assigned_by': Select(attrs={'class': 'form-control'}),
#            #'assigned_to': Select(attrs={'class': 'form-control'}),
#            #'manager': Select(attrs={'class': 'form-control'}),
#            #'title': CharField(attrs={'max_length': 200, 'required': False}),
#        }

#    def save(self):
#        instance = super(EvidenceCreateForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not Evidence.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        instance.save()
#        update_change_reason(instance, 'Initial Evidence Creation')
#        return instance


#class EvidenceEditForm(forms.ModelForm):

#    change_reason = CharField(required=False, label='Reason For Change',)
#    title = CharField(max_length=200, required=False,)
#    reference = CharField(max_length=200, required=False,)
#    description = CharField(required=False,)
   
#    class Meta:
#        model = Evidence
#        fields = ['title', 'reference','comment', 'bag_number', 'location', 'uri',
#                 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
#                'slug', 'type', 'status', 'classification', 'priority', 'authorisation',
#               'category', 'chain_of_custody', 'assigned_to', 'custodian', 'assigned_by']
#        labels = {
#            'type': _('Evidence Type'),
#            'title':_('Title'),
#            'reference':_('Reference'),
#            'background':_('Background'),
#            'location':_('Location'),
#            'description':_('Description'),
#            'brief':_('Brief'),
#        }
#        error_messages = {
#            'evidence': {'max_length': _("The Evidence Type is Invalid"),},
#        }
#        help_texts = {
#            'title': _('Some useful help text.'),
#        }
#        widgets = {
#            'authorisation': Select(attrs={'class': 'form-control'}),
#            'priority': Select(attrs={'class': 'form-control'}),
#            'classification': Select(attrs={'class': 'form-control'}),
#            'status': Select(attrs={'class': 'form-control'}),
#            'type': Select(attrs={'class': 'form-control'}),
#            'assigned_by': Select(attrs={'class': 'form-control'}),
#            'assigned_to': Select(attrs={'class': 'form-control'}),
#            'manager': Select(attrs={'class': 'form-control'}),
#            'image_upload': FileInput(attrs={'class': 'form-control'}),
#            #'title': CharField(attrs={'max_length': 200, 'required': False}),
#        }

#    def save(self):
#        instance = super(EvidenceEditForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not Evidence.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        changereason = self.cleaned_data['change_reason']
#        instance.save()
#        update_change_reason(instance, 'Initial Evidence Creation')
#        return instance

    
##class EvidenceNoteCreateForm(forms.ModelForm):
    
##    def __init__(self,*args,**kwargs):
##        self.evidence = kwargs.pop('evidence')
##        super(EvidenceNoteCreateForm,self).__init__(*args,**kwargs)
##        self.fields['evidence'].widget = forms.TextInput(attrs={'evidence': self.evidence})

##    title = CharField(max_length=200, required=False, label='Title',)
    
        
##    class Meta:
##        model = EvidenceNote
##        fields = ['title', 'slug', 'image_upload', 'private', 'type', 'status', 'classification', 'priority', 'category', 'authorisation', 'assigned_to', 'manager', 'assigned_by', 'description', 'evidence']

##    def save(self):
##        instance = super(EvidenceNoteCreateForm, self).save(commit=False)
##        instance.slug = orig = slugify(instance.title)
##        for x in itertools.count(1):
##            if not EvidenceNote.objects.filter(slug=instance.slug).exists():
##                break
##            instance.slug = '%s-%d' % (orig, x)
##        instance.evidence = self.evidence
##        #changereason = self.cleaned_data['change_reason']
##        instance.save()
##        #update_change_reason(instance, changereason)
##        return instance


##class EvidenceTaskCreateForm(forms.ModelForm):

##    title = CharField(max_length=200, required=False, label='Title',)
##    background = CharField(required=False, label='Background',)
##    location = CharField(max_length=200, required=False, label='Location',)
##    description = CharField(required=False, label='Description',)
##    change_reason = CharField(required=False, label='Reason For Change',)

##    class Meta:
##        model = EvidenceTask
##        fields = ['title', 'background', 'location', 'description', 'private', 'type', 'status', 'priority', 'authorisation',]

##    def save(self):
##        instance = super(EvidenceTaskForm, self).save(commit=False)
##        instance.slug = orig = slugify(instance.title)
##        for x in itertools.count(1):
##            if not EvidenceTask.objects.filter(slug=instance.slug).exists():
##                break
##            instance.slug = '%s-%d' % (orig, x)
##        changereason = self.cleaned_data['change_reason']
##        instance.save()
##        update_change_reason(instance, changereason)
##        return instance