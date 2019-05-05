"""
Case Entity Forms.
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

""" Case Person
'description', 'role', 'type', 'person', 'case', 'notes',
'private'
"""

""" Case Company
'description', 'role', 'type', 'company', 'case', 'notes',
'private'
"""


class CustomCheckbox(Field):
	template = 'global/forms/custom_checkbox.html'


# Case Person
class __BasePersonForm(forms.ModelForm):
	
	class Meta:
		model = CasePerson
		fields = ['description', 'role', 'type', 'person', 'private']


class BasePersonForm(__BasePersonForm):
	
	def __init__(self, *args, **kwargs):
		super(BasePersonForm, self).__init__(*args, **kwargs)
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

                # Description
				Field(
                    'description',
                    id="description-field", 
					css_class="descriptionfield",
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Description"),
					wrapper_class='col-md-9'),

                # Role
				Field(
                    "role",
                    id="role-field", 
					css_class="rolefield",
					autocomplete='on',
					title=self.fields['role'].help_text,
					placeholder=_("Role"),
					wrapper_class='col-md-9'),
                
                # Type
				Field(
                    'type',
                    id="type-field", 
					css_class="typefield",
					autocomplete='on',
					title=self.fields['type'].help_text,
					placeholder=_("Type"),
					wrapper_class='col-md-9'),

                # Person
				Field(
                    "person",
                    id="person-field", 
					css_class="personfield",
					autocomplete='on',
					title=self.fields['person'].help_text,
					placeholder=_("Person"),
					wrapper_class='col-md-9'),

                # Private
				CustomCheckbox(
					"private",
					title=self.fields['private'].help_text),

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


class CasePersonCreateForm(BasePersonForm):
	
	def save(self):
		instance = super(CasePersonCreateForm, self).save(commit=False)
		changereason = 'Initial Creation'
		instance.save()
		update_change_reason(instance, changereason)
		return instance


class CasePersonUpdateForm(BasePersonForm):
	
	change_reason = CharField(required=False, label='Reason For Change',)

	def save(self):
		instance = super(CasePersonUpdateForm, self).save(commit=False)
		changereason = self.cleaned_data['change_reason']
		instance.save()
		update_change_reason(instance, changereason)
		return instance


# Case Company
class __BaseCompanyForm(forms.ModelForm):
		
	class Meta:
		model = CaseCompany
		fields = ['description', 'role', 'type', 'company', 'case',
                'private']


class BaseCompanyForm(__BaseCompanyForm):
	
	def __init__(self, *args, **kwargs):
		super(BaseCompanyForm, self).__init__(*args, **kwargs)
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

                # Description
				Field(
                    'description',
                    id="description-field", 
					css_class="descriptionfield",
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Description"),
					wrapper_class='col-md-9'),

                # Role
				Field(
                    "role",
                    id="role-field", 
					css_class="rolefield",
					autocomplete='on',
					title=self.fields['role'].help_text,
					placeholder=_("Role"),
					wrapper_class='col-md-9'),
                
                # Type
				Field(
                    'type',
                    id="type-field", 
					css_class="typefield",
					autocomplete='on',
					title=self.fields['type'].help_text,
					placeholder=_("Type"),
					wrapper_class='col-md-9'),

                # Company
				Field(
                    "company",
                    id="company-field", 
					css_class="companyfield",
					autocomplete='on',
					title=self.fields['company'].help_text,
					placeholder=_("Company"),
					wrapper_class='col-md-9'),

                # Private
				CustomCheckbox(
					"private",
					title=self.fields['private'].help_text),

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

   
class CaseCompanyCreateForm(BaseCompanyForm):
 
	def save(self):
		instance = super(CaseCompanyCreateForm, self).save(commit=False)
		changereason = 'Initial Creation'
		instance.save()
		update_change_reason(instance, changereason)
		return instance


class CaseCompanyUpdateForm(BaseCompanyForm):
	
	change_reason = CharField(required=False, label='Reason For Change',)

	def save(self):
		instance = super(CaseCompanyUpdateForm, self).save(commit=False)
		changereason = self.cleaned_data['change_reason']
		instance.save()
		update_change_reason(instance, changereason)
		return instance
