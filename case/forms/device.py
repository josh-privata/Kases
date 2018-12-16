"""
Case Device Forms.
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

""" Case Device
'active', 'device', 'case', 'note',
'description', 'private'
"""


class CustomCheckbox(Field):
	template = 'global/forms/custom_checkbox.html'


# Case Device
class __BaseForm(forms.ModelForm):
	
	class Meta:
		model = CaseInventory
		fields = ('active', 'device',
				'description', 'private')


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

                # Description
				Field(
                    'description',
                    id="description-field", 
					css_class="descriptionfield",
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Description"),
					wrapper_class='col-md-9'),

                # Device
				Field(
                    "device",
                    id="device-field", 
					css_class="devicefield",
					autocomplete='on',
					title=self.fields['device'].help_text,
					placeholder=_("Device"),
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


class CaseDeviceCreateForm(BaseForm):
	
	def save(self):
		instance = super(CaseDeviceCreateForm, self).save(commit=False)
		changereason = _('Initial Creation')
		instance.save()
		update_change_reason(instance, changereason)
		return instance


class CaseDeviceUpdateForm(BaseForm):
	
	change_reason = CharField(required=False, label=_('Reason For Change'),)

	def save(self):
		instance = super(CaseDeviceUpdateForm, self).save(commit=False)
		changereason = _(self.cleaned_data['change_reason'])
		instance.save()
		update_change_reason(instance, changereason)
		return instance
