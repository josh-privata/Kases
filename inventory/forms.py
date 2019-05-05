## Inventory Forms ##

import itertools
from django import forms
from django.utils import timezone
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
from inventory.models import  Device
from inventory.models import ServiceContract
from inventory.models import Service

''' Device
'title', 'manufacturer', 'model', 'variation', 'serial_number',
'status', 'condition', 'returnable', 'internal_id',
'model_number', 'purchased', 'manual', 'description'
'warranty_title', 'warranty_id', 'warranty_terms', 'warranty_duration',
'warranty_start', 'warranty_end', 'warranty_extended', 'warranty_document',
'warranty_contact', 'warranty_vendor', 'warranty_responsible',
'sales_rep', 'vendor', 'service_contract', 'subcategory', 'category',
'authorisation', 'manager', 'device_dependecy', 'related_devices'
'''

''' Service Contract
'title', 'internal_id', 'service_id', 'terms', 'contract_start',
'contract_end', 'renewal_cost', 'active', 'description',
'vendor', 'contact', 'document', 'responsible',
'''
	
''' Service
'issue', 'resolution', 'status', 'technician', 'leave_date',
'return_date', 'cost', 'invoice', 'receipt', 'returned',
'under_warranty', 'tested', 'description', 
'vendor', 'service_contract','manager', 'tested_by'
'''


class CustomCheckbox(Field):
	template = 'global/forms/custom_checkbox.html'


## Device Forms
class BaseDevice(forms.ModelForm):
		
	class Meta:
		model = Device
		fields = ('title', 'manufacturer', 'model', 'variation', 'serial_number',
			'status', 'condition', 'returnable', 'internal_id',
			'model_number', 'purchased', 'description',
			'warranty_title', 'warranty_id', 'warranty_terms', 'warranty_duration',
			'warranty_start', 'warranty_end', 'warranty_extended',
			'warranty_contact', 'warranty_vendor', 'warranty_responsible',
			'sales_rep', 'vendor', 'service_contract', 'subcategory', 'category',
			'authorisation', 'manager')


class DeviceForm(BaseDevice):
	
	def __init__(self, *args, **kwargs):
		super(DeviceForm, self).__init__(*args, **kwargs)
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

				# Manufacturer
				Field(
					'manufacturer',
					id="manufacturer-field", 
					css_class="manufacturerfield", 
					autocomplete='on',
					title=self.fields['manufacturer'].help_text,
					placeholder=_("Manufacturer"),
					wrapper_class='col-md-9'),

				# Model
				Field(
					'model',
					id="model-field", 
					css_class="modelfield", 
					autocomplete='on',
					title=self.fields['model'].help_text,
					placeholder=_("Model"),
					wrapper_class='col-md-9'),

				# Variation
				Field(
					'variation',
					id="variation-field", 
					css_class="variationfield", 
					autocomplete='on',
					title=self.fields['variation'].help_text,
					placeholder=_("Variation"),
					wrapper_class='col-md-9'),

				# Serial Number
				Field(
					'serial_number',
					id="serial_number-field", 
					css_class="serial_numberfield", 
					autocomplete='on',
					title=self.fields['serial_number'].help_text,
					placeholder=_("Serial Number"),
					wrapper_class='col-md-9'),

				# Description
				Field(
					"description",
					id="description-field", 
					css_class="descriptionfield", 
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Case Description"),
					rows="3",
					wrapper_class='col-md-9'),
				
    #            # Manual
				#Field(
				#	"manual",
				#	id="manual-field",
				#	css_class="manualfield", 
				#	autocomplete='on',
				#	title=self.fields['manual'].help_text,
				#	placeholder=_("Manual Upload"),
				#	wrapper_class='col-md-9',),
				#HTML(u"""{% load i18n %}
				#			<p class="help-block">
				#			{% trans "Available formats are PDF, DOCX, DOC and TXT." %}
				#			</p>"""),
                
                # Condition
				Field(
					"condition",
					id="condition-field", 
					css_class="conditionfield", 
					autocomplete='on',
					title=self.fields['condition'].help_text,
					placeholder=_("Condition"),
					rows="3",
					wrapper_class='col-md-9'),
                
                # Internal ID
				Field(
					"internal_id",
					id="internal_id-field", 
					css_class="internal_idfield", 
					autocomplete='on',
					title=self.fields['internal_id'].help_text,
					placeholder=_("Internal ID"),
					rows="3",
					wrapper_class='col-md-9'),
                
                # Model Number
				Field(
					"model_number",
					id="model_number-field", 
					css_class="model_numberfield", 
					autocomplete='on',
					title=self.fields['model_number'].help_text,
					placeholder=_("Model Number"),
					rows="3",
					wrapper_class='col-md-9'),
                
                # Purchased
				Field(
					"purchased",
					id="purchased-field", 
					css_class="purchasedfield", 
					autocomplete='on',
					title=self.fields['purchased'].help_text,
					placeholder=_("Purchased"),
					rows="3",
					wrapper_class='col-md-9'),
                
                # Sales Rep
				Field(
					"sales_rep",
					id="sales_rep-field", 
					css_class="sales_repfield", 
					autocomplete='on',
					title=self.fields['sales_rep'].help_text,
					placeholder=_("Sales Representative"),
					rows="3",
					wrapper_class='col-md-9'),
                
                # Vendor
				Field(
					"vendor",
					id="vendor-field", 
					css_class="vendorfield", 
					autocomplete='on',
					title=self.fields['vendor'].help_text,
					placeholder=_("Vendor"),
					rows="3",
					wrapper_class='col-md-9'),

				# Returnable
				CustomCheckbox(
					"returnable",
					title=self.fields['returnable'].help_text),

                # Warranty Title     
				Field(
					'warranty_title', 
					id="warranty_title-field", 
					css_class="warranty_titlefield",
					autocomplete='on',
					title=self.fields['warranty_title'].help_text,
					placeholder=_("Warranty Title"),
					wrapper_class='col-md-9'),

				# Warranty ID
				Field(
					'warranty_id',
					id="warranty_id-field", 
					css_class="warranty_idfield", 
					autocomplete='on',
					title=self.fields['warranty_id'].help_text,
					placeholder=_("Warranty ID"),
					wrapper_class='col-md-9'),

				# Warranty Duration
				Field(
					'warranty_duration',
					id="warranty_duration-field", 
					css_class="warranty_durationfield", 
					autocomplete='on',
					title=self.fields['warranty_duration'].help_text,
					placeholder=_("Warranty Duration"),
					wrapper_class='col-md-9'),

				# Warranty Start
				Field(
					'warranty_start',
					id="warranty_start-field", 
					css_class="warranty_startfield", 
					autocomplete='on',
					title=self.fields['warranty_start'].help_text,
					placeholder=_("Warranty Start"),
					wrapper_class='col-md-9'),

				# warranty_end
				Field(
					'warranty_end',
					id="warranty_end-field", 
					css_class="warranty_endfield", 
					autocomplete='on',
					title=self.fields['warranty_end'].help_text,
					placeholder=_("warranty_end"),
					wrapper_class='col-md-9'),

				# Warranty Extended
				CustomCheckbox(
					"warranty_extended",
					title=self.fields['warranty_extended'].help_text),

                # Warranty Terms
				Field(
					"warranty_terms",
					id="warranty_terms-field", 
					css_class="warranty_termsfield", 
					autocomplete='on',
					title=self.fields['warranty_terms'].help_text,
					placeholder=_("Warranty Terms"),
					wrapper_class='col-md-9'),

				# Warranty Contact
				Field(
					"warranty_contact",
					id="warranty_contact-field", 
					css_class="warranty_contactfield", 
					autocomplete='on',
					title=self.fields['warranty_contact'].help_text,
					placeholder=_("Warranty Contact"),
					wrapper_class='col-md-9'),

				# Warranty Vendor
				Field(
					"warranty_vendor",
					id="warranty_vendor-field",
					css_class="warranty_vendor_tofield", 
					autocomplete='on',
					title=self.fields['warranty_vendor'].help_text,
					placeholder=_("Warranty Vendor"),
					wrapper_class='col-md-9'), 

				# Warranty Responsible
				Field(
					"warranty_responsible",
					id="warranty_responsible-field",
					css_class="warranty_responsible_field", 
					autocomplete='on',
					title=self.fields['warranty_responsible'].help_text,
					placeholder=_("Warranty Responsible"),
					wrapper_class='col-md-9'),

				## Warranty Document
				#Field(
				#	"warranty_document",
				#	id="warranty_document-field",
				#	css_class="warranty_documentfield", 
				#	autocomplete='on',
				#	title=self.fields['warranty_document'].help_text,
				#	placeholder=_("Warranty Document Upload"),
				#	wrapper_class='col-md-9',),
				#HTML(u"""{% load i18n %}
				#			<p class="help-block">
				#			{% trans "Available formats are PDF, DOCX, DOC and TXT." %}
				#			</p>"""),
 
				# Service Contract
				Field(
					"service_contract",
					id="service_contract-field", 
					css_class="service_contractfield", 
					autocomplete='on',
					title=self.fields['service_contract'].help_text,
					placeholder=_("Service Contract"),
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
						placeholder=_("Status"),
						wrapper_class='col-md-9')),

				# Manager
				Div(
					PrependedText(
						"manager", 
						_(""),
						id="manager-field",
						css_class="managerfield", 
						autocomplete='on',
						title=self.fields['manager'].help_text,
						placeholder=_("Manager"),
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
						placeholder=_("Category"),
						wrapper_class='col-md-9')),
                
                # Subcategory
				Div(
					PrependedText(
						"subcategory", 
						_(""),
						id="subcategory-field",
						css_class="subcategoryfield", 
						autocomplete='on',
						title=self.fields['subcategory'].help_text,
						placeholder=_("Subcategory"),
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
						placeholder=_("Authorisation"),
						wrapper_class='col-md-9'))
			),

			FormActions(Submit("submit", _("Save")),))
		
		# Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class DeviceCreateForm(DeviceForm):
	
	def save(self):
		instance = super(DeviceCreateForm, self).save(commit=False)
		changereason = 'Initial Creation'
		instance.save()
		update_change_reason(instance, changereason)
		return instance


class DeviceUpdateForm(DeviceForm):
	
	change_reason = CharField(required=False, label='Reason For Change',)
	
	def save(self):
		instance = super(DeviceUpdateForm, self).save(commit=False)
		changereason = self.cleaned_data['change_reason']
		instance.save()
		update_change_reason(instance, changereason)
		return instance

## Service Forms
class BaseServiceContract(forms.ModelForm):
	
	class Meta:
		model = ServiceContract
		fields = ('title', 'internal_id', 'service_id', 'terms', 'contract_start',
				'contract_end', 'renewal_cost', 'active', 'description',
				'vendor', 'contact', 'responsible',)


class BaseService(forms.ModelForm):
	
	class Meta:
		model = Service
		fields = ('issue', 'resolution', 'status', 'technician', 'leave_date',
				'return_date', 'cost', 'returned',
				'under_warranty', 'tested', 'description', 
				'vendor', 'service_contract','manager', 'tested_by')


class ServiceContractForm(BaseServiceContract):
	
	def __init__(self, *args, **kwargs):
		super(ServiceContractForm, self).__init__(*args, **kwargs)
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

				# Service ID
				Field(
					'service_id',
					id="service_id-field", 
					css_class="service_idfield", 
					autocomplete='on',
					title=self.fields['service_id'].help_text,
					placeholder=_("Service ID"),
					wrapper_class='col-md-9'),

				# Terms
				Field(
					'terms',
					id="terms-field", 
					css_class="termsfield", 
					autocomplete='on',
					title=self.fields['terms'].help_text,
					placeholder=_("Terms"),
					wrapper_class='col-md-9'),

				# Contract Start
				Field(
					'contract_start',
					id="contract_start-field", 
					css_class="contract_startfield", 
					autocomplete='on',
					title=self.fields['contract_start'].help_text,
					placeholder=_("Contract Start"),
					wrapper_class='col-md-9'),

				# Contract End
				Field(
					'contract_end',
					id="contract_end-field", 
					css_class="contract_endfield", 
					autocomplete='on',
					title=self.fields['contract_end'].help_text,
					placeholder=_("Contract End"),
					wrapper_class='col-md-9'),

				# Renewal Cost
				Field(
					"renewal_cost",
					id="renewal_cost-field", 
					css_class="renewal_costfield", 
					autocomplete='on',
					title=self.fields['renewal_cost'].help_text,
					placeholder=_("Renewal Cost"),
					rows="3",
					wrapper_class='col-md-9'),
				
                # Description
				Field(
					"description",
					id="description-field",
					css_class="descriptionfield", 
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Description"),
					wrapper_class='col-md-9',),
                
                # Vendor
				Field(
					"vendor",
					id="vendor-field", 
					css_class="vendorfield", 
					autocomplete='on',
					title=self.fields['vendor'].help_text,
					placeholder=_("Vendor"),
					wrapper_class='col-md-9'),
                
                # Internal ID
				Field(
					"internal_id",
					id="internal_id-field", 
					css_class="internal_idfield", 
					autocomplete='on',
					title=self.fields['internal_id'].help_text,
					placeholder=_("Internal ID"),
					wrapper_class='col-md-9'),
                
                # Contact
				Field(
					"contact",
					id="contact-field", 
					css_class="contactfield", 
					autocomplete='on',
					title=self.fields['contact'].help_text,
					placeholder=_("Contact"),
					wrapper_class='col-md-9'),
                
                # Responsible
				Field(
					"responsible",
					id="responsible-field", 
					css_class="responsiblefield", 
					autocomplete='on',
					title=self.fields['responsible'].help_text,
					placeholder=_("Responsible"),
					wrapper_class='col-md-9'),
                
				# Active
				CustomCheckbox(
					"active",
					title=self.fields['active'].help_text),

			),

			FormActions(Submit("submit", _("Save")),))
		
		# Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class ServiceForm(BaseService):
	
	def __init__(self, *args, **kwargs):
		super(ServiceForm, self).__init__(*args, **kwargs)
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
						
				# Issue     
				Field(
					'issue', 
					id="issue-field", 
					css_class="issuefield",
					autocomplete='on',
					title=self.fields['issue'].help_text,
					placeholder=_("Issue"),
					wrapper_class='col-md-9'),

				# Resolution
				Field(
					'resolution',
					id="resolution-field", 
					css_class="resolutionfield", 
					autocomplete='on',
					title=self.fields['resolution'].help_text,
					placeholder=_("Resolution"),
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

				# Technician
				Field(
					'technician',
					id="technician-field", 
					css_class="technicianfield", 
					autocomplete='on',
					title=self.fields['technician'].help_text,
					placeholder=_("Technician"),
					wrapper_class='col-md-9'),

				# Leave Date
				Field(
					'leave_date',
					id="leave_date-field", 
					css_class="leave_datefield", 
					autocomplete='on',
					title=self.fields['leave_date'].help_text,
					placeholder=_("Leave Date"),
					wrapper_class='col-md-9'),

				# Return Date
				Field(
					"return_date",
					id="return_date-field", 
					css_class="return_datefield", 
					autocomplete='on',
					title=self.fields['return_date'].help_text,
					placeholder=_("Return Date"),
					rows="3",
					wrapper_class='col-md-9'),
				
                # Description
				Field(
					"description",
					id="description-field",
					css_class="descriptionfield", 
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Description"),
					wrapper_class='col-md-9',),
                
                # Vendor
				Field(
					"vendor",
					id="vendor-field", 
					css_class="vendorfield", 
					autocomplete='on',
					title=self.fields['vendor'].help_text,
					placeholder=_("Vendor"),
					wrapper_class='col-md-9'),
                
                # Service Contract
				Field(
					"service_contract",
					id="service_contract-field", 
					css_class="service_contractfield", 
					autocomplete='on',
					title=self.fields['service_contract'].help_text,
					placeholder=_("Service Contract"),
					wrapper_class='col-md-9'),
                
                # Manager
				Field(
					"manager",
					id="manager-field", 
					css_class="managerfield", 
					autocomplete='on',
					title=self.fields['manager'].help_text,
					placeholder=_("Manager"),
					wrapper_class='col-md-9'),
                
                # Tested By
				Field(
					"tested_by",
					id="tested_by-field", 
					css_class="tested_byfield", 
					autocomplete='on',
					title=self.fields['tested_by'].help_text,
					placeholder=_("Tested By"),
					wrapper_class='col-md-9'),
                
                
                # Tested
				CustomCheckbox(
					"tested",
					title=self.fields['tested'].help_text),
                
                # Under Warranty
				CustomCheckbox(
					"under_warranty",
					title=self.fields['under_warranty'].help_text),

				# Returned
				CustomCheckbox(
					"returned",
					title=self.fields['returned'].help_text),

			),

			FormActions(Submit("submit", _("Save")),))
		
		# Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None