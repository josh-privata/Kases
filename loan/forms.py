## Loan Forms ##

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
from loan.models import  Loan


''' Loan 
'approver_note', 'return_note', 'booked_from', 'booked_until',
'date_taken', 'date_returned', 'original_condition', 'return_condition',
'status', 'returned', 'taken', 'case', 'device', 'loaned_to',
'loaned_by', 'taken_by', 'returned_by', 'private', 'description'
'''

class CustomCheckbox(Field):
	template = 'global/forms/custom_checkbox.html'


## Base Forms
class __BaseForm(forms.ModelForm):
	
	class Meta:
		model = Loan
		fields = ('approver_note', 'return_note', 'booked_from',
				 'booked_until', 'date_taken', 'date_returned', 'description',
				 'original_condition', 'return_condition','status',
				 'returned', 'taken', 'case', 'device', 'loaned_to',
				 'loaned_by', 'taken_by', 'returned_by', 'private')


class BaseForm(__BaseForm):

	def __init__(self, *args, **kwargs):
		super(BaseForm, self).__init__(*args, **kwargs)
		user = kwargs.pop('user', None)
		#if user.groups.filter(name='Investigator').exists():
		#	self.fields['status'].choices = (
  #                                              (LOAN_PENDING, 'Awaiting Loan Approval'),
  #                                              (LOAN_WITHDRAWN, 'Loan Withdrawn'),
  #                                              (LOAN_CLOSED, 'Loan Closed'),
  #                                              (RETURN_PENDING, 'Awaiting Return Approval'),
  #                                              (RETURN_WITHDRAWN, 'Return Withdrawn'),
  #                                          )
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
						
				# Approver Note
				Field(
					'approver_note', 
					id="approver_note-field", 
					css_class="approver_notefield",
					autocomplete='on',
					title=self.fields['approver_note'].help_text,
					placeholder=_("Approver Note"),
					wrapper_class='col-md-9'),

				# Return Note
				Field(
					'return_note',
					id="return_note-field", 
					css_class="return_notefield", 
					autocomplete='on',
					title=self.fields['return_note'].help_text,
					placeholder=_("Return Note"),
					wrapper_class='col-md-9'),

				# Booked From
				Field(
					'booked_from',
					id="booked_from-field", 
					css_class="booked_fromfield", 
					autocomplete='on',
					title=self.fields['booked_from'].help_text,
					placeholder=_("Booked From"),
					wrapper_class='col-md-9'),

				# Booked Until
				Field(
					'booked_until',
					id="booked_until-field", 
					css_class="booked_untilfield", 
					autocomplete='on',
					title=self.fields['booked_until'].help_text,
					placeholder=_("Booked Until"),
					wrapper_class='col-md-9'),
				
				# Date Taken
				Div(
					PrependedText(
						"date_taken", 
						_(""),
						id="date_taken-field",
						css_class="date_takenfield", 
						autocomplete='on',
						title=self.fields['date_taken'].help_text,
						placeholder=_("Date Taken"),
						wrapper_class='col-md-9')),

				# Date Returned
				Div(
					PrependedText(
						"date_returned", 
						_(""),
						id="date_returned-field",
						css_class="date_returnedfield", 
						autocomplete='on',
						title=self.fields['date_returned'].help_text,
						placeholder=_("Date Returned"),
						wrapper_class='col-md-9')),

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

				# Returned
				CustomCheckbox(
					"returned",
					title=self.fields['returned'].help_text),
				
				# Taken
				CustomCheckbox(
					"taken",
					title=self.fields['taken'].help_text),

				# Loaned To
				Field(
					"loaned_to",
					id="loaned_to-field", 
					css_class="loaned_tofield", 
					autocomplete='on',
					title=self.fields['loaned_to'].help_text,
					placeholder=_("Loaned To"),
					wrapper_class='col-md-9'),

				# Returned By
				Field(
					"returned_by",
					id="returned_by-field",
					css_class="returned_byfield", 
					autocomplete='on',
					title=self.fields['returned_by'].help_text,
					placeholder=_("Returned By"),
					wrapper_class='col-md-9'), 

				# Loaned By
				Field(
					"loaned_by",
					id="loaned_by-field",
					css_class="loaned_by_field", 
					autocomplete='on',
					title=self.fields['loaned_by'].help_text,
					placeholder=_("Loaned By"),
					wrapper_class='col-md-9'),

				# Taken By
				Field(
					"taken_by",
					id="taken_by-field",
					css_class="taken_byfield", 
					autocomplete='on',
					title=self.fields['taken_by'].help_text,
					placeholder=_("Taken By"),
					wrapper_class='col-md-9',),
 
				# Device
				Field(
					"device",
					id="device-field", 
					css_class="devicefield", 
					autocomplete='on',
					title=self.fields['device'].help_text,
					placeholder=_("Device"),
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

				# Case
				Div(
					PrependedText(
						"case", 
						_(""),
						id="case-field",
						css_class="casefield", 
						autocomplete='on',
						title=self.fields['case'].help_text,
						placeholder=_("Case"),
						wrapper_class='col-md-9')),

				# Return Condition
				Div(
					PrependedText(
						"return_condition", 
						_(""),
						id="return_condition-field",
						css_class="return_conditionfield", 
						autocomplete='on',
						title=self.fields['return_condition'].help_text,
						placeholder=_("Return Condition"),
						wrapper_class='col-md-9')),

				# Original Condition
				Div(
					PrependedText(
						"original_condition", 
						_(""),
						id="original_condition-field",
						css_class="original_conditionfield", 
						autocomplete='on',
						title=self.fields['original_condition'].help_text,
						placeholder=_("Original Condition"),
						wrapper_class='col-md-9')),

			),

			FormActions(Submit("submit", _("Save")),))
		
		# Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class LoanCreateForm(BaseForm):
	
	def save(self):
		instance = super(LoanCreateForm, self).save(commit=False)
		changereason = 'Initial Creation'
		instance.save()
		update_change_reason(instance, changereason)
		return instance


class LoanUpdateForm(BaseForm):
	
	change_reason = CharField(required=False, label='Reason For Change',)

	def save(self):
		instance = super(LoanUpdateForm, self).save(commit=False)
		changereason = self.cleaned_data['change_reason']
		instance.save()
		update_change_reason(instance, changereason)
		return instance


## Loan With Case Forms
class LoanWithCaseCreateForm(LoanCreateForm):

	class Meta:
		model = Loan
		fields = ('approver_note', 'return_note', 'booked_from',
				 'booked_until', 'date_taken', 'date_returned', 'description',
				 'original_condition', 'return_condition','status',
				 'returned', 'taken', 'loaned_to', 'loaned_by', 'device',
				 'taken_by', 'returned_by', 'private', 'case')


class LoanWithCaseUpdateForm(LoanUpdateForm):

	class Meta:
		model = Loan
		fields = ('approver_note', 'return_note', 'booked_from',
				 'booked_until', 'date_taken', 'date_returned', 'description',
				 'original_condition', 'return_condition','status',
				 'returned', 'taken', 'loaned_to', 'loaned_by', 'device',
				 'taken_by', 'returned_by', 'private')


## Loan With Device Forms
class LoanWithDeviceCreateForm(LoanCreateForm):
	
	class Meta:
		model = Loan
		fields = ('approver_note', 'return_note', 'booked_from',
				 'booked_until', 'date_taken', 'date_returned', 'description',
				 'original_condition', 'return_condition','status',
				 'returned', 'taken', 'loaned_to', 'loaned_by', 'case',
				 'taken_by', 'returned_by', 'private')


class LoanWithDeviceUpdateForm(LoanUpdateForm):

	class Meta:
		model = Loan
		fields = ('approver_note', 'return_note', 'booked_from',
				 'booked_until', 'date_taken', 'date_returned', 'description',
				 'original_condition', 'return_condition','status',
				 'returned', 'taken', 'loaned_to', 'loaned_by', 'case',
				 'taken_by', 'returned_by', 'private')


## Loan With Both Forms
class LoanWithBothCreateForm(LoanCreateForm):
	
	class Meta:
		model = Loan
		fields = ('approver_note', 'return_note', 'booked_from',
				 'booked_until', 'date_taken', 'date_returned', 'description',
				 'original_condition', 'return_condition','status',
				 'returned', 'taken', 'loaned_to', 'loaned_by', 
				 'taken_by', 'returned_by', 'private')


class LoanWithBothUpdateForm(LoanUpdateForm):

	class Meta:
		model = Loan
		fields = ('approver_note', 'return_note', 'booked_from',
				 'booked_until', 'date_taken', 'date_returned', 'description',
				 'original_condition', 'return_condition','status',
				 'returned', 'taken', 'loaned_to', 'loaned_by', 
				 'taken_by', 'returned_by', 'private')
