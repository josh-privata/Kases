## Case Event Forms ##

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

""" Case Event
'title', 'image_upload', 'description', 'private', 'date',
'case', 'person', 'company', 'evidence', 'status', 'priority',
'authorisation', 'manager', 'assigned_by', 'assigned_to',
"""

class CustomCheckbox(Field):
	template = 'global/forms/custom_checkbox.html'


# Case Event
class __BaseForm(forms.ModelForm):
   
	class Meta:
		model = CaseEvent
		fields = ['title', 'image_upload', 'description', 'private', 'date',
                'person', 'company', 'evidence', 'status', 'priority',
                'authorisation', 'manager', 'assigned_by', 'assigned_to']


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
					placeholder=_("Title"),
					wrapper_class='col-md-9'),

                # Description
				Field(
                    'description',
                    id="description-field", 
					css_class="descriptionfield",
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Description"),
					wrapper_class='col-md-9'),

                # Image Upload
				Field(
                    "image_upload",
                    id="image_upload-field", 
					css_class="image_uploadfield",
					autocomplete='on',
					title=self.fields['image_upload'].help_text,
					placeholder=_("Image Upload"),
					wrapper_class='col-md-9'),

                # Private
				CustomCheckbox(
					"private",
					title=self.fields['private'].help_text),

                # Date
				Field(
                    'date', 
					id="date-field", 
					css_class="datefield",
					autocomplete='on',
					title=self.fields['date'].help_text,
					placeholder=_("Date"),
					wrapper_class='col-md-9'),

                # Person
				Field(
                    'person', 
					id="person-field", 
					css_class="personfield",
					autocomplete='on',
					title=self.fields['person'].help_text,
					placeholder=_("Person"),
					wrapper_class='col-md-9'),

                # Company
				Field(
                    'company', 
					id="company-field", 
					css_class="companyfield",
					autocomplete='on',
					title=self.fields['company'].help_text,
					placeholder=_("Company"),
					wrapper_class='col-md-9'),

                # Evidence
				Field(
                    'evidence', 
					id="evidence-field", 
					css_class="evidencefield",
					autocomplete='on',
					title=self.fields['evidence'].help_text,
					placeholder=_("Evidence"),
					wrapper_class='col-md-9'),

                # Status
				Field(
                    'status', 
					id="status-field", 
					css_class="statusfield",
					autocomplete='on',
					title=self.fields['status'].help_text,
					placeholder=_("Status"),
					wrapper_class='col-md-9'),

                # Priority
				Field(
                    'priority', 
					id="priority-field", 
					css_class="priorityfield",
					autocomplete='on',
					title=self.fields['priority'].help_text,
					placeholder=_("Priority"),
					wrapper_class='col-md-9'),

                # Authorisation
				Field(
                    'authorisation', 
					id="authorisation-field", 
					css_class="authorisationfield",
					autocomplete='on',
					title=self.fields['authorisation'].help_text,
					placeholder=_("Authorisation"),
					wrapper_class='col-md-9'),

                # Manager
				Field(
                    'manager', 
					id="manager-field", 
					css_class="managerfield",
					autocomplete='on',
					title=self.fields['manager'].help_text,
					placeholder=_("Manager"),
					wrapper_class='col-md-9'),

                # Assigned By
				Field(
                    'assigned_by', 
					id="assigned_by-field", 
					css_class="assigned_byfield",
					autocomplete='on',
					title=self.fields['assigned_by'].help_text,
					placeholder=_("Assigned By"),
					wrapper_class='col-md-9'),

                # Assigned To
				Field(
                    'assigned_to', 
					id="assigned_to-field", 
					css_class="assigned_tofield",
					autocomplete='on',
					title=self.fields['assigned_to'].help_text,
					placeholder=_("Assigned To"),
					wrapper_class='col-md-9'),

                # Change Reason
				Field(
                    'change_reason',
                    id="change_reason-field", 
					css_class="change_reasonfield",
					autocomplete='on',
					title=_('Reason for change'),
					placeholder=_('Please enter a reason for making the changes'),
					wrapper_class='col-md-9'),
			),

			FormActions(Submit("submit", _("Save")),))

        # Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class CaseEventCreateForm(BaseForm):

	def save(self):
		instance = super(CaseEventCreateForm, self).save(commit=False)
		instance.save()
		update_change_reason(instance, 'Initial Event Creation')
		#self.save_m2m()
		return instance


class CaseEventUpdateForm(BaseForm):
	
	change_reason = CharField(required=False, label='Reason For Change',)

	def save(self):
		instance = super(CaseEventUpdateForm, self).save(commit=False)
		changereason = self.cleaned_data['change_reason']
		instance.save()
		update_change_reason(instance, changereason)
		#self.save_m2m()
		return instance
