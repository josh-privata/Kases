## Case Forms ##

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
from crispy_forms.layout import Submit
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
			Fieldset(
                (),
						
			    # Title     
			    Field(
				    'title', 
				    id="title-field", 
				    css_class="titlefield",
				    autocomplete='on',
				    title=self.fields['title'].help_text,
				    placeholder=_("Case Title"),
				    wrapper_class='col-md-9'),

			    # Reference
			    Field(
				    'reference',
				    id="reference-field", 
				    css_class="referencefield", 
				    autocomplete='on',
				    title=self.fields['reference'].help_text,
				    placeholder=_("Reference Number"),
				    wrapper_class='col-md-9'),

			    # Background
			    Field(
				    'background',
				    id="background-field", 
				    css_class="backgroundfield", 
				    autocomplete='on',
				    title=self.fields['background'].help_text,
				    placeholder=_("Case Background"),
				    rows="3",
				    wrapper_class='col-md-9'),

			    # Purpose
			    Field(
				    'purpose',
				    id="purpose-field", 
				    css_class="purposefield", 
				    autocomplete='on',
				    title=self.fields['purpose'].help_text,
				    placeholder=_("Case Purpose"),
				    wrapper_class='col-md-9'),

			    # Change Reason
			    Field(
				    'change_reason',
				    id="change_reason-field", 
				    css_class="change_reasonfield", 
				    autocomplete='on',
				    title=_('Please enter a reason for making the changes'),
				    placeholder=_("Change Reason"),
				    wrapper_class='col-md-9'),

			    # Description
			    Field(
				    "description",
				    id="description-field", 
				    css_class="input-blocklevel descriptionfield", 
				    autocomplete='on',
				    title=self.fields['description'].help_text,
				    placeholder=_("Case Description"),
				    rows="3",
				    wrapper_class='col-md-9'),

			    # Private
			    CustomCheckbox(
				    "private",
				    title=self.fields['private'].help_text),

			    # Assigned By
			    Field(
				    "assigned_by",
				    id="assigned_by-field", 
				    css_class="input-blocklevel assigned_byfield", 
				    autocomplete='on',
				    title=self.fields['assigned_by'].help_text,
				    placeholder=_("Case Assigned By"),
				    wrapper_class='col-md-9'),

			    # Assigned To
			    Field(
				    "assigned_to",
				    id="assigned_to-field",
				    css_class="input-blocklevel assigned_tofield", 
				    autocomplete='on',
				    title=self.fields['assigned_to'].help_text,
				    placeholder=_("Case Assigned To"),
				    wrapper_class='col-md-9'), 

			    # Manager
			    Field(
				    "manager",
				    id="manager-field",
				    css_class="input-blocklevel manager_field", 
				    autocomplete='on',
				    title=self.fields['manager'].help_text,
				    placeholder=_("Case Manager"),
				    wrapper_class='col-md-9'),

			    # Image Upload
			    Field(
				    "image_upload",
				    id="image_upload-field",
				    css_class="input-blocklevel image_uploadfield", 
				    autocomplete='on',
				    title=self.fields['image_upload'].help_text,
				    placeholder=_("Case Image Upload"),
				    wrapper_class='col-md-9',),
			    HTML(u"""{% load i18n %}
						    <p class="help-block">
						    {% trans "Available formats are JPG, GIF, and PNG. Minimal size is 800 × 800 px." %}
						    </p>"""),
 
			    # Type
			    Field(
				    "type",
				    id="type-field", 
				    css_class="input-blocklevel typefield", 
				    autocomplete='on',
				    title=self.fields['type'].help_text,
				    placeholder=_("Case Type"),
				    wrapper_class='col-md-9'),

			    # Status
			    Div(
				    PrependedText(
					    "status", 
					    _(""), 
					    id="status-field",
					    css_class="input-blocklevel statusfield", 
					    autocomplete='on',
					    title=self.fields['status'].help_text,
					    placeholder=_("Case Status"),
					    wrapper_class='col-md-9')),

			    # Classification
			    Div(
				    PrependedText(
					    "classification", 
					    _(""),
					    id="classification-field",
					    css_class="input-blocklevel classificationfield", 
					    autocomplete='on',
					    title=self.fields['classification'].help_text,
					    placeholder=_("Case Classification"),
					    wrapper_class='col-md-9')),

			    # Priority
			    Div(
				    PrependedText(
					    "priority", 
					    _(""),
					    id="priority-field",
					    css_class="input-blocklevel priorityfield", 
					    autocomplete='on',
					    title=self.fields['priority'].help_text,
					    placeholder=_("Case Priority"),
					    wrapper_class='col-md-9')),

			    # Category
			    Div(
				    PrependedText(
					    "category", 
					    _(""),
					    id="category-field",
					    css_class="input-blocklevel categoryfield", 
					    autocomplete='on',
					    title=self.fields['category'].help_text,
					    placeholder=_("Case Category"),
					    wrapper_class='col-md-9')),

			    # Authorisation
			    Div(
				    PrependedText(
					    "authorisation", 
					    _(""),
					    id="authorisation-field",
					    css_class="input-blocklevel authorisationfield", 
					    autocomplete='on',
					    title=self.fields['authorisation'].help_text,
					    placeholder=_("Case Authorisation"),
					    wrapper_class='col-md-9'))
			),

			FormActions(Submit("submit", _("Save")),))
		
		# Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class CaseForm(BaseForm):
	
	def save(self):
		instance = super(CaseForm, self).save(commit=False)
		instance.save()
		update_change_reason(instance, 'Initial Case Creation')
		return instance


class CaseUpdateForm(BaseForm):
	
	change_reason = CharField(required=False, label=_('Reason For Change'),)

	def save(self):
		instance = super(CaseUpdateForm, self).save(commit=False)
		changereason = _(self.cleaned_data['change_reason'])
		instance.save()
		update_change_reason(instance, changereason)
		return instance
