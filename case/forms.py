"""
Case Forms.
"""

import itertools
from django import forms
from django import forms
from django.forms import CharField, Select, FileInput, modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from crispy_forms import layout, bootstrap
from crispy_forms.helper import FormHelper
from simple_history.utils import update_change_reason
from case.models import Case, CaseInventory
from case.models import CaseNote, CaseTask, CaseEvidence, CaseCompany, CasePerson, CaseEvent, EventPerson


""" Case
'brief', 'description'
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'private'
"""

""" Case Person
'role', 'notes', 'type', 'person', 'case', 'linked_by', 'brief', 'description'
"""

""" Case Company
'role', 'notes', 'type', 'company', 'case', 'linked_by', 'brief', 'description'
"""

""" Case Device
'reason', 'description', 'expected_use', 'device', 'linked_by'
"""

""" Case Evidence
'title', 'reference', 'comment', 'bag_number', 'location',
'uri', 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
'retention_date', 'brief', 'custodian', 'chain_of_custody',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'assigned_by',
'description', 'private'
"""

""" Case Task
'title', 'background', 'location', 'brief',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'description', 'private', 'note', 'person', 'company', 'inventory',
'evidence
"""

""" Case Note
'title', 'image_upload', 'brief',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'description', 'private'
"""

""" Case Event
'title', 'image_upload', 'brief',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'description', 'private', 'person', 'company', 'evidence'
"""


# Case
class CaseForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(CaseForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_action = ""
		self.helper.form_method = "POST"
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8'
		self.helper.layout = layout.Layout(
			
			layout.Div(layout.Fieldset(_("Main data"),
						layout.Field('title', wrapper_class='col-md-9'),
						layout.Field('reference', wrapper_class='col-md-9'),
						layout.Field('background', wrapper_class='col-md-9'),
						layout.Field('purpose', wrapper_class='col-md-9'),
                        layout.Field('change_reason', wrapper_class='col-md-9'),
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


class __CaseCreateForm(forms.ModelForm):

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

    
class CrispyCaseForm(CaseForm):
	
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


class CrispyCaseUpdateForm(CaseForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CrispyCaseUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Case.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, 'Initial Case Creation')
        return instance


class CaseCreateForm(__CaseCreateForm):

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


class CaseUpdateForm(__CaseCreateForm):

    change_reason = CharField(required=False, label='Reason For Change',)

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
class CaseNoteForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CaseNoteForm, self).__init__(*args, **kwargs)
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
                        layout.Field('change_reason', wrapper_class='col-md-9'),
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


class __CaseNoteForm(forms.ModelForm):
    
    class Meta:
        model = CaseNote
        fields = ['title', 'image_upload', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private']


class CrispyCaseNoteCreateForm(CaseNoteForm):

    def save(self):
        instance = super(CrispyCaseNoteCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseNote.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Note Creation')
        self.save_m2m()
        return instance


class CrispyCaseNoteUpdateForm(CaseNoteForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CrispyCaseNoteUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseNote.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        self.save_m2m()
        return instance


class CaseNoteCreateForm(__CaseNoteForm):
        
    title = CharField(max_length=200, required=False, label='Title',)

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


class CaseNoteUpdateForm(__CaseNoteForm):
        
    title = CharField(max_length=200, required=False, label='Title',)
    change_reason = CharField(required=False, label='Reason For Change',)

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


# Case Event
class CaseEventForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CaseEventForm, self).__init__(*args, **kwargs)
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
                        layout.Field('change_reason', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Main data"),
                          layout.Field("description"),
                          layout.Field("status", css_class="input-blocklevel", rows="3"),
                          layout.Field("classification"),
                          layout.Field("priority"),),
            
            layout.Fieldset(_("Poop"), 
                          layout.Field("person"),
                          layout.Field("evidence"),
                          layout.Field("company"),),

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
        model = CaseEvent
        fields = ['title', 'image_upload', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private', 'person', 'company', 'evidence']


class __CaseEventForm(forms.ModelForm):
   
    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CaseEvent
        fields = ['title', 'image_upload', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private', 'company', 'evidence']


class CrispyCaseEventCreateForm(CaseEventForm):

    def save(self):
        instance = super(CrispyCaseEventCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvent.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Event Creation')
        self.save_m2m()
        return instance


class CrispyCaseEventUpdateForm(CaseEventForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CrispyCaseEventUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvent.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        self.save_m2m()
        return instance


class CaseEventCreateForm(__CaseEventForm):

    def save(self):
        instance = super(CaseEventCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvent.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        #changereason = self.cleaned_data['change_reason']
        instance.save()
        #update_change_reason(instance, changereason)
        return instance


class CaseEventUpdateForm(__CaseEventForm):
        
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CaseEventUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvent.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


EventPersonFormset = modelformset_factory(
    EventPerson,
    fields=('person', 'role', 'notes', 'type' ),
    # case, event, linked_by
    extra=1,
    #widgets={
    #    'name': forms.TextInput(
    #        attrs={
    #            'class': 'form-control',
    #            'placeholder': 'Enter Author Name here'
    #        }
    #    )
    #}
)


# Case Task
class CaseTaskForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CaseTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('title'),
                        layout.Field('background'),
                        layout.Field('location'),
                        layout.Field('change_reason'),
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

            layout.Fieldset(_("Poop"), 
                          layout.Field("note"),
                          layout.Field("event"),
                          layout.Field("person"),
                          layout.Field("company"),
                          layout.Field("inventory"),
                          layout.Field("evidence"),),

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
                  'description', 'private', 'note', 'person', 'company', 'inventory',
                  'evidence']


class __CaseTaskForm(forms.ModelForm):

    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CaseTask
        fields = ['title', 'background', 'location', 'brief',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
                  'description', 'private', 'note', 'person', 'company', 'inventory',
                  'evidence']

        
class CrispyCaseTaskCreateForm(CaseTaskForm):

    def save(self):
        instance = super(CrispyCaseTaskCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseTask.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Task Creation')
        self.save_m2m()
        return instance


class CrispyCaseTaskUpdateForm(CaseTaskForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CrispyCaseTaskUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseTask.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        self.save_m2m()
        return instance


class CaseTaskCreateForm(__CaseTaskForm):

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


class CaseTaskUpdateForm(__CaseTaskForm):

    change_reason = CharField(required=False, label='Reason For Change',)

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
class CaseEvidenceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CaseEvidenceForm, self).__init__(*args, **kwargs)
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
                        layout.Field('change_reason', wrapper_class='col-md-9'),
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


class __CaseEvidenceForm(forms.ModelForm):

    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CaseEvidence
        fields = ['title', 'reference', 'comment', 'bag_number', 'location',
                  'uri', 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
                  'retention_date', 'brief', 'custodian', 'chain_of_custody',
                  'type', 'status', 'classification', 'priority', 'category',
                  'authorisation', 'assigned_to', 'assigned_by',
                  'description', 'private']


class CrispyCaseEvidenceCreateForm(CaseEvidenceForm):
   
    def save(self):
        instance = super(CrispyCaseEvidenceCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvidence.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Evidence Creation')
        self.save_m2m()
        return instance


class CrispyCaseEvidenceUpdateForm(CaseEvidenceForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CrispyCaseEvidenceUpdateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not CaseEvidence.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        self.save_m2m()
        return instance


class CaseEvidenceCreateForm(__CaseEvidenceForm):

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


class CaseEvidenceUpdateForm(__CaseEvidenceForm):

    change_reason = CharField(required=False, label='Reason For Change',)
   
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


# Case Person
class CasePersonForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CasePersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('role', wrapper_class='col-md-6'),
                        layout.Field('description', wrapper_class='col-md-6'),
                        layout.Field('notes', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("type"),
                          layout.Field("person"),
                          layout.Field("linked_by"),
                          layout.Field('change_reason', wrapper_class='col-md-6'),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = CasePerson
        fields = ['role', 'notes', 'type', 'person', 'linked_by', 'description']


class __CasePersonForm(forms.ModelForm):
    
    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CasePerson
        fields = ['role', 'notes', 'type', 'person', 'linked_by', 'description']


class CrispyCasePersonCreateForm(CasePersonForm):
    
    def save(self):
        instance = super(CrispyCasePersonCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CrispyCasePersonUpdateForm(CasePersonForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CrispyCasePersonUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CasePersonCreateForm(__CasePersonForm):
  
    def save(self):
        instance = super(CasePersonCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CasePersonUpdateForm(__CasePersonForm):

    change_reason = CharField(required=False, label='Reason For Change',)
    
    def save(self):
        instance = super(CasePersonUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


# Case Company
class CaseCompanyForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CaseCompanyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('role', wrapper_class='col-md-6'),
                        layout.Field('description', wrapper_class='col-md-6'),
                        layout.Field('notes', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("type"),
                          layout.Field("company"),
                          layout.Field("linked_by"),
                          layout.Field('change_reason', wrapper_class='col-md-6'),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = CaseCompany
        fields = ['role', 'notes', 'type', 'company', 'linked_by', 'description']

   
class __CaseCompanyForm(forms.ModelForm):
        
    class Meta:
        model = CaseCompany
        fields = ['role', 'notes', 'type', 'company', 'linked_by', 'description']


class CrispyCaseCompanyCreateForm(CaseCompanyForm):
 
    def save(self):
        instance = super(CrispyCaseCompanyCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CrispyCaseCompanyUpdateForm(CaseCompanyForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CrispyCaseCompanyUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CaseCompanyCreateForm(__CaseCompanyForm):
      
    def save(self):
        instance = super(CaseCompanyCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CaseCompanyUpdateForm(__CaseCompanyForm):

    change_reason = CharField(required=False, label='Reason For Change',)
    
    def save(self):
        instance = super(CaseCompanyUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


# Case Device
class CaseDeviceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CaseDeviceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('reason', wrapper_class='col-md-6'),
                        layout.Field('description', wrapper_class='col-md-6'),
                        layout.Field('expected_use', wrapper_class='col-md-9'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("device"),
                          layout.Field("linked_by"),
                          layout.Field('change_reason', wrapper_class='col-md-6'),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = CaseInventory
        fields = ['reason', 'description', 'expected_use', 'device', 'linked_by']


class __CaseDeviceForm(forms.ModelForm):
        
    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CaseInventory
        fields = ('reason', 'description', 'expected_use', 'device', 'linked_by')


class CrispyCaseDeviceCreateForm(CaseDeviceForm):
    
    def save(self):
        instance = super(CrispyCaseDeviceCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CrispyCaseDeviceUpdateForm(CaseDeviceForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CrispyCaseDeviceUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CaseDeviceCreateForm(__CaseDeviceForm):
        
    #def __init__(self, casepk=None, *args, **kwargs):
    #    super(CaseDeviceCreateForm,self).__init__(*args,**kwargs)
    #    self.case = Case.objects.get(id=kwargs['casepk'])
    title = CharField(max_length=200, required=False, label='Title',)
    
    class Meta:
        model = CaseInventory
        fields = ('reason', 'description', 'expected_use', 'device', 'linked_by')

    def save(self):
        instance = super(CaseDeviceCreateForm, self).save(commit=False)
        changereason = 'Initial Creation'
        instance.save()
        update_change_reason(instance, changereason)
        return instance


class CaseDeviceUpdateForm(__CaseDeviceForm):

    change_reason = CharField(required=False, label='Reason For Change',)
    
    class Meta:
        model = CaseInventory
        fields = ('reason', 'description', 'expected_use', 'device', 'linked_by')

    def save(self):
        instance = super(CaseDeviceUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        return instance
