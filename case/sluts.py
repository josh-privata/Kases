"""
Case Forms.
"""

import itertools
from django import forms
from django.forms import CharField
from django.forms import Select
from django.forms import FileInput
from django.forms import TextInput
from django.forms import PasswordInput
from django.forms import BooleanField
from django.forms import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from crispy_forms import layout
from crispy_forms import bootstrap 
from crispy_forms.bootstrap import PrependedText
from crispy_forms.bootstrap import AppendedText
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Div
from crispy_forms.layout import HTML
from simple_history.utils import update_change_reason
from bootstrap_datepicker_plus import DateTimePickerInput
from case.models import Case
from case.models import CaseInventory
from case.models import CaseTask
from case.models import CaseEvidence
from case.models import CaseCompany
from case.models import CasePerson
from case.models import CaseEvent
#from case.models import CaseNote

""" Date Time Usage
	date_field = DatePickerInput(
		options={
			"format": "MM/DD/YYYY", # moment date-time format
			"showClose": True,
			"showClear": True,
			"showTodayButton": True,
		}			   // or //	widgets = {		'start_date':DatePickerInput().start_of('event days'),
		'end_date':DatePickerInput().end_of('event days'),
		'start_time':TimePickerInput().start_of('party time'),
		'end_time':TimePickerInput().end_of('party time'),		'start_date': DatePickerInput(),
		'start_time': TimePickerInput(),
		'start_datetime': DateTimePickerInput(),
		'start_month': MonthPickerInput(),
		'start_year': YearPickerInput(),		}	)

"""

""" Case
'title', 'reference', 'description', 'background', 'purpose',
'image_upload', 'private',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'deadline', 'note', 'judge',
"""

""" Case Person
'description', 'role', 'type', 'person', 'case', 'notes',
'private'
"""

""" Case Company
'description', 'role', 'type', 'company', 'case', 'notes',
'private'
"""

""" Case Device
'description', 'active', 'device', 'case', 'note',
'private'
"""

""" Case Evidence
'case', 'title', 'reference', 'bag_number', 'location',
'image_upload', 'qr_code', 'retention_reminder_sent', 'retention_start_date',
'retention_end_date', 'chain_of_custody', 'description', 'private',
'type', 'status', 'priority', 'authorisation',
'custodian', 'assigned_by', 'assigned_to',
'note', 'file_location'
"""

""" Case Task
'title', 'location', 'description', 'private',
'case', 'event', 'device', 'evidence', 'person', 'company',
'category', 'status', 'priority', 'authorisation',
'manager', 'assigned_by', 'assigned_to',
'note', 'deadline'
"""

""" Case Event
'title', 'image_upload', 'description', 'private',
'case', 'person', 'company', 'evidence', 'status', 'priority',
'authorisation', 'manager', 'assigned_by', 'assigned_to',
'note', 'deadline'
"""

class CustomCheckbox(Field):
	template = 'global/forms/custom_checkbox.html'


# Case
class __BaseForm(forms.ModelForm):

	class Meta:
		model = Case
		fields = ['title', 'reference', 'description', 'background', 'purpose',
					'image_upload', 'private',
					'type', 'status', 'classification', 'priority', 'category',
					'authorisation', 'assigned_to', 'manager', 'assigned_by']


class BaseForm(__BaseForm):
	
	def __init__(self, *args, **kwargs):
		super(BaseForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_action = ""
		self.helper.form_method = "POST"
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8'
		self.helper.layout = Layout(
			
			# Fields
			#Div(
				Fieldset((),
						
				# Title     
				Field(
					'title', 
					id="title-field", 
					css_class="titlefield",
					autocomplete='on',
					title=self.fields['title'].help_text,
					placeholder="Case Title",
					wrapper_class='col-md-9'),

				# Reference
				Field(
					'reference',
					id="reference-field", 
					css_class="referencefield", 
					autocomplete='on',
					title=self.fields['reference'].help_text,
					placeholder="Reference Number",
					wrapper_class='col-md-9'),

				# Background
				Field(
					'background',
					id="background-field", 
					css_class="backgroundfield", 
					autocomplete='on',
					title=self.fields['background'].help_text,
					placeholder="Case Background",
					rows="3",
					wrapper_class='col-md-9'),

				# Purpose
				Field(
					'purpose',
					id="purpose-field", 
					css_class="purposefield", 
					autocomplete='on',
					title=self.fields['purpose'].help_text,
					placeholder="Case Purpose",
					wrapper_class='col-md-9'),

				# Change Reason
				Field(
					'change_reason',
					id="change_reason-field", 
					css_class="change_reasonfield", 
					autocomplete='on',
					title='Please enter a reason for making the changes',
					placeholder="Change Reason",
					wrapper_class='col-md-9'),

				# Description
				Field(
					"description",
					id="description-field", 
					css_class="input-blocklevel descriptionfield", 
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder="Case Description",
					rows="3",
					wrapper_class='col-md-9'),

				# Private
				CustomCheckbox(
					"private",
					title=self.fields['private'].help_text),

				# Type
				Field(
					"type",
					id="type-field", 
					css_class="input-blocklevel typefield", 
					autocomplete='on',
					title=self.fields['type'].help_text,
					placeholder="Case Type",
					wrapper_class='col-md-9'),

				# Assigned By
				Field(
					"assigned_by",
					id="assigned_by-field", 
					css_class="input-blocklevel assigned_byfield", 
					autocomplete='on',
					title=self.fields['assigned_by'].help_text,
					placeholder="Case Assigned By",
					wrapper_class='col-md-9'),

				# Assigned To
				Field(
					"assigned_to",
					id="assigned_to-field",
					css_class="input-blocklevel assigned_tofield", 
					autocomplete='on',
					title=self.fields['assigned_to'].help_text,
					placeholder="Case Assigned To",
					wrapper_class='col-md-9'), 

				# Manager
				Field(
					"manager",
					id="manager-field",
					css_class="input-blocklevel manager_field", 
					autocomplete='on',
					title=self.fields['manager'].help_text,
					placeholder="Case Manager",
					wrapper_class='col-md-9'),

				# Image Upload
				Field(
					"image_upload",
					id="image_upload-field",
					css_class="input-blocklevel image_uploadfield", 
					autocomplete='on',
					title=self.fields['image_upload'].help_text,
					placeholder="Case Image Upload",
					wrapper_class='col-md-9',),
				HTML(u"""{% load i18n %}
							<p class="help-block">
							{% trans "Available formats are JPG, GIF, and PNG. Minimal size is 800 × 800 px." %}
							</p>"""),

				# Status
				Div(
					PrependedText(
						"status", 
						"", 
						id="status-field",
						css_class="input-blocklevel statusfield", 
						autocomplete='on',
						title=self.fields['status'].help_text,
						placeholder="Case Status",
						wrapper_class='col-md-9')),

				# Classification
				Div(
					PrependedText(
						"classification", 
						"", 
						id="classification-field",
						css_class="input-blocklevel classificationfield", 
						autocomplete='on',
						title=self.fields['classification'].help_text,
						placeholder="Case Classification",
						wrapper_class='col-md-9')),

				# Priority
				Div(
					PrependedText(
						"priority", 
						"", 
						id="priority-field",
						css_class="input-blocklevel priorityfield", 
						autocomplete='on',
						title=self.fields['priority'].help_text,
						placeholder="Case Priority",
						wrapper_class='col-md-9')),

				# Category
				Div(
					PrependedText(
						"category", 
						"", 
						id="category-field",
						css_class="input-blocklevel categoryfield", 
						autocomplete='on',
						title=self.fields['category'].help_text,
						placeholder="Case Category",
						wrapper_class='col-md-9')),

				# Authorisation
				Div(
					PrependedText(
						"authorisation", 
						"", 
						id="authorisation-field",
						css_class="input-blocklevel authorisationfield", 
						autocomplete='on',
						title=self.fields['authorisation'].help_text,
						placeholder="Case Authorisation",
						wrapper_class='col-md-9'))

				)
			,

			FormActions(layout.Submit("submit", _("Save")),))
		
		# Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class CrispyCaseForm(BaseForm):
	
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


class CrispyCaseUpdateForm(BaseForm):
	
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
		update_change_reason(instance, changereason)
		return instance


class CaseCreateForm(__BaseForm):

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


class CaseUpdateForm(__BaseForm):

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
#class CaseNoteForm(forms.ModelForm):
	
#    def __init__(self, *args, **kwargs):
#        super(CaseNoteForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_action = ""
#        self.helper.form_method = "POST"
#        self.helper.form_class = 'form-horizontal'
#        self.helper.label_class = 'col-lg-2'
#        self.helper.field_class = 'col-lg-8'
#        self.helper.layout = layout.Layout(
			
#            layout.Div(layout.Fieldset(_("Main data"),
#                        layout.Field('title', wrapper_class='col-md-6'),
#                        layout.Field('brief', wrapper_class='col-md-6'),
#                        layout.Field('type', wrapper_class='col-md-9'),
#                        layout.Field('change_reason', wrapper_class='col-md-9'),
#                        #css_class='form-row'
#                        )),

#            layout.Fieldset(_("Main data"),
#                          layout.Field("description"),
#                          layout.Field("status", css_class="input-blocklevel", rows="3"),
#                          layout.Field("classification"),
#                          layout.Field("priority"),),

#            layout.Fieldset(_("Image"),
#                          layout.Field("image_upload", css_class="input-block-level"),
#                          layout.HTML(u"""{% load i18n %}
#                            <p class="help-block">
#                                {% trans "Available formats are JPG, GIF, and PNG. Minimal size is 800 × 800 px." %}
#                            </p>"""),
#                          title=_("Image upload"), css_id="image_fieldset",),

#            layout.Fieldset(_("Authorisation"), 
#                          layout.Field("category"),
#                          layout.Field("authorisation"),
#                          layout.Field("assigned_to"),
#                          layout.Field("manager"),
#                          layout.Field("assigned_by"),
#                          layout.Field("assigned_to"),
#                          layout.Field("private"),),

#            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

#    class Meta:
#        model = CaseNote
#        fields = ['title', 'image_upload', 'brief',
#                  'type', 'status', 'classification', 'priority', 'category',
#                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
#                  'description', 'private']


#class __CaseNoteForm(forms.ModelForm):
	
#    class Meta:
#        model = CaseNote
#        fields = ['title', 'image_upload', 'brief',
#                  'type', 'status', 'classification', 'priority', 'category',
#                  'authorisation', 'assigned_to', 'manager', 'assigned_by',
#                  'description', 'private']


#class CrispyCaseNoteCreateForm(CaseNoteForm):

#    def save(self):
#        instance = super(CrispyCaseNoteCreateForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not CaseNote.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        instance.save()
#        update_change_reason(instance, 'Initial Note Creation')
#        self.save_m2m()
#        return instance


#class CrispyCaseNoteUpdateForm(CaseNoteForm):
	
#    change_reason = CharField(required=False, label='Reason For Change',)

#    def save(self):
#        instance = super(CrispyCaseNoteUpdateForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not CaseNote.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        changereason = self.cleaned_data['change_reason']
#        instance.save()
#        update_change_reason(instance, changereason)
#        self.save_m2m()
#        return instance


#class CaseNoteCreateForm(__CaseNoteForm):
		
#    title = CharField(max_length=200, required=False, label='Title',)

#    def save(self):
#        instance = super(CaseNoteCreateForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not CaseNote.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        #changereason = self.cleaned_data['change_reason']
#        instance.save()
#        #update_change_reason(instance, changereason)
#        return instance


#class CaseNoteUpdateForm(__CaseNoteForm):
		
#    title = CharField(max_length=200, required=False, label='Title',)
#    change_reason = CharField(required=False, label='Reason For Change',)

#    def save(self):
#        instance = super(CaseNoteUpdateForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not CaseNote.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        changereason = self.cleaned_data['change_reason']
#        instance.save()
#        update_change_reason(instance, changereason)
#        return instance


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
		fields = ['title', 'image_upload', 'description', 'private',
			'case', 'person', 'company', 'evidence', 'status', 'priority',
			'authorisation', 'manager', 'assigned_by', 'assigned_to',
			'note']


class __CaseEventForm(forms.ModelForm):
   
	title = CharField(max_length=200, required=False, label='Title',)
	
	class Meta:
		model = CaseEvent
		fields = ['title', 'image_upload', 'description', 'private',
			'case', 'person', 'company', 'evidence', 'status', 'priority',
			'authorisation', 'manager', 'assigned_by', 'assigned_to',
			'note']


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
		#self.save_m2m()
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
		#self.save_m2m()
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
						layout.Field('location'),
						layout.Field('change_reason'),
						#css_class='form-row'
						)),

			layout.Fieldset(_("Main data"),
						  layout.Field("category"),
						  layout.Field("status"),),

			layout.Fieldset(_("Image"),
						  layout.Field("image_upload", css_class="input-block-level"),
						  layout.HTML(u"""{% load i18n %}
							<p class="help-block">
								{% trans "Available formats are JPG, GIF, and PNG. Minimal size is 800 × 800 px." %}
							</p>"""),
						  title=_("Image upload"), css_id="image_fieldset",),

			layout.Fieldset(_("Poop"), 
						  layout.Field("event"),
						  layout.Field("person"),
						  layout.Field("company"),
						  layout.Field("inventory"),
						  layout.Field("evidence"),),

			layout.Fieldset(_("Authorisation"), 
						  layout.Field("priority"),
						  layout.Field("authorisation"),
						  layout.Field("assigned_to"),
						  layout.Field("manager"),
						  layout.Field("assigned_by"),
						  layout.Field("description"),
						  layout.Field("private"),),

			bootstrap.FormActions(layout.Submit("submit", _("Save")),))

	class Meta:
		model = CaseTask
		fields = ['title', 'location', 'description', 'private',
			'case', 'event', 'device', 'evidence', 'person', 'company',
			'category', 'status', 'priority', 'authorisation',
			'manager', 'assigned_by', 'assigned_to',
			'note']


class __CaseTaskForm(forms.ModelForm):

	title = CharField(max_length=200, required=False, label='Title',)
	
	class Meta:
		model = CaseTask
		fields = ['title', 'location', 'description', 'private',
			'case', 'event', 'device', 'evidence', 'person', 'company',
			'category', 'status', 'priority', 'authorisation',
			'manager', 'assigned_by', 'assigned_to',
			'note']

		
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
						layout.Field('change_reason', wrapper_class='col-md-9'),
						#css_class='form-row'
						)),

			layout.Div(layout.Fieldset(_("Main data"),
						layout.Field('bag_number', wrapper_class='col-md-6'),
						layout.Field('location', wrapper_class='col-md-6'),
						#css_class='form-row'
						)),

			layout.Div(layout.Fieldset(_("Main data"),
						layout.Field('qr_code', wrapper_class='col-md-6'),
						#css_class='form-row'
						)),

			layout.Div(layout.Fieldset(_("Main data"),
						layout.Field('retention_end_date', wrapper_class='col-md-6'),
						layout.Field('retention_start_date', wrapper_class='col-md-6'),
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
		fields = ['case', 'title', 'reference', 'bag_number', 'location',
					'image_upload', 'qr_code', 'retention_reminder_sent', 'retention_start_date',
					'retention_end_date', 'chain_of_custody', 'description', 'private',
					'type', 'status', 'priority', 'authorisation',
					'custodian', 'assigned_by', 'assigned_to',
					'note']


class __CaseEvidenceForm(forms.ModelForm):

	title = CharField(max_length=200, required=False, label='Title',)
	
	class Meta:
		model = CaseEvidence
		fields = ['case', 'title', 'reference', 'bag_number', 'location',
					'image_upload', 'qr_code', 'retention_reminder_sent', 'retention_start_date',
					'retention_end_date', 'chain_of_custody', 'description', 'private',
					'type', 'status', 'priority', 'authorisation',
					'custodian', 'assigned_by', 'assigned_to',
					'note']


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
						layout.Field('notes', wrapper_class='col-md-9'),)),

			layout.Fieldset(_("Authorisation"), 
						  layout.Field("type"),
						  layout.Field("person"),
						  layout.Field("linked_by"),
						  layout.Field('change_reason', wrapper_class='col-md-6'),),

			bootstrap.FormActions(layout.Submit("submit", _("Save")),))

	class Meta:
		model = CasePerson
		fields = ['description', 'role', 'type', 'person', 'case', 'private']


class __CasePersonForm(forms.ModelForm):
	
	title = CharField(max_length=200, required=False, label='Title',)
	
	class Meta:
		model = CasePerson
		fields = ['description', 'role', 'type', 'person', 'case', 'private']


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
		fields = ['description', 'role', 'type', 'company', 'case', 'private']

   
class __CaseCompanyForm(forms.ModelForm):
		
	class Meta:
		model = CaseCompany
		fields = ['description', 'role', 'type', 'company', 'case', 'private']


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
						#css_class='form-row'
						)),

			layout.Fieldset(_("Authorisation"), 
						  layout.Field("device"),
						  layout.Field("linked_by"),
						  layout.Field('change_reason', wrapper_class='col-md-6'),),

			bootstrap.FormActions(layout.Submit("submit", _("Save")),))

	class Meta:
		model = CaseInventory
		fields = ['description', 'active', 'device', 'case', 'note',
					'private']


class __CaseDeviceForm(forms.ModelForm):
		
	title = CharField(max_length=200, required=False, label='Title',)
	
	class Meta:
		model = CaseInventory
		fields = ('description', 'active', 'device', 'case', 'note',
					'private')


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
		
	def save(self):
		instance = super(CaseDeviceCreateForm, self).save(commit=False)
		changereason = 'Initial Creation'
		instance.save()
		update_change_reason(instance, changereason)
		return instance


class CaseDeviceUpdateForm(__CaseDeviceForm):

	change_reason = CharField(required=False, label='Reason For Change',)

	def save(self):
		instance = super(CaseDeviceUpdateForm, self).save(commit=False)
		changereason = self.cleaned_data['change_reason']
		instance.save()
		update_change_reason(instance, changereason)
		return instance
