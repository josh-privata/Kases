## Entity Forms ##
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
from crispy_forms.helper import FormHelper
from simple_history.utils import update_change_reason
from simple_history.models import HistoricalRecords
from bootstrap_datepicker_plus import DateTimePickerInput
from entity.models.person import Person
from entity.models.entity import Address
from entity.models.entity import Telephone
from entity.models.entity import Email
from entity.models.entity import Website
from entity.models.entity import Social
from entity.models.company import Company
#import vobject

''' Person
'prefix', 'first_name', 'last_name', 'middle_names',
'suffix', 'nickname', 'aliases',
'gender', 'dob', 'height', 'weight', 'age',
'description', 'taxfile', 'spouse', 'image_upload',
'type', 'status', 'classification', 'category',
'authorisation', 'employment', 'affiliations',
'address', 'telephone', 'email', 'website', 'social'
'''

''' Company
'title', 'code', 'logo_upload', 'industry', 'description',
'type', 'status', 'classification', 'category', 'authorisation',
'social', 'address', 'telephone', 'email', 'website',
'''

''' Employment
'job_title', 'notes', 'date_start', 'date_finish',
'salary', 'current', 'company'
'''

''' Address
'line1', 'line2', 'line3', 'city', 'state', 'country', 
'postcode', 'type', 'location', 'primary', 'current'
'''

''' Telephone
'number', 'type', 'primary', 'current'
'''

''' Email
'email', 'location', 'primary', 'current'
'''

''' Social
'service', 'alias', 'url', 'primary', 'current'
'''

''' Website
'url', 'primary', 'current'
'''


class CustomCheckbox(Field):
	template = 'global/forms/custom_checkbox.html'


# Entity Forms
class BaseAddress(forms.ModelForm):

	class Meta:
		model = Address
		fields = ['line1', 'line2', 'line3', 'city', 'state', 'country', 
				'postcode', 'type', 'location', 'primary', 'current']


class BaseEmail(forms.ModelForm):

	class Meta:
		model = Email
		fields = ['email', 'location', 'primary', 'current']


class BaseWebsite(forms.ModelForm):

	class Meta:
		model = Website
		fields = ['url', 'primary', 'current']
		

class BaseSocial(forms.ModelForm):

	class Meta:
		model = Social
		fields = ['service', 'alias', 'url', 'primary', 'current']


class BaseTelephone(forms.ModelForm):

	class Meta:
		model = Telephone
		fields = ['number', 'type', 'primary', 'current']


class AddressForm(BaseAddress):
		
	def __init__(self, *args, **kwargs):
		super(AddressForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = Layout(
						  
			# Fields
			Fieldset(
				(),
						
				# Line 1     
				Field(
					'line1', 
					id="line1-field", 
					css_class="line1field",
					autocomplete='on',
					title=self.fields['line1'].help_text,
					placeholder=_("Line 1"),
					wrapper_class='col-md-9'),

				# Line 2
				Field(
					'line2',
					id="line2-field", 
					css_class="line2field", 
					autocomplete='on',
					title=self.fields['line2'].help_text,
					placeholder=_("Line 2"),
					wrapper_class='col-md-9'),

				# Line 3
				Field(
					'line3',
					id="line3-field", 
					css_class="line3field", 
					autocomplete='on',
					title=self.fields['line3'].help_text,
					placeholder=_("Line 3"),
					wrapper_class='col-md-9'),

				# City
				Field(
					'city',
					id="city-field", 
					css_class="cityfield", 
					autocomplete='on',
					title=self.fields['city'].help_text,
					placeholder=_("City"),
					wrapper_class='col-md-9'),

				# State
				Field(
					'state',
					id="state-field", 
					css_class="statefield", 
					autocomplete='on',
					title=self.fields['state'].help_text,
					placeholder=_("State"),
					wrapper_class='col-md-9'),

				# Country
				Field(
					"country",
					id="country-field", 
					css_class="countryfield", 
					autocomplete='on',
					title=self.fields['country'].help_text,
					placeholder=_("Country"),
					wrapper_class='col-md-9'),

				# Postcode
				Field(
					"postcode",
					id="postcode-field", 
					css_class="postcoded_byfield", 
					autocomplete='on',
					title=self.fields['postcode'].help_text,
					placeholder=_("Postcode"),
					wrapper_class='col-md-9'),

				# Type
				Field(
					"type",
					id="type-field",
					css_class="typefield", 
					autocomplete='on',
					title=self.fields['type'].help_text,
					placeholder=_("Type"),
					wrapper_class='col-md-9'), 

				# Location
				Field(
					"location",
					id="location-field",
					css_class="location_field", 
					autocomplete='on',
					title=self.fields['location'].help_text,
					placeholder=_("Location"),
					wrapper_class='col-md-9'),

				# Primary
				CustomCheckbox(
					"primary",
					title=self.fields['primary'].help_text),

				# Current
				CustomCheckbox(
					"current",
					title=self.fields['current'].help_text),
			),)

        # Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class EmailForm(BaseEmail):
		
	def __init__(self, *args, **kwargs):
		super(EmailForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = Layout(

			# Fields
			Fieldset(
				(),
						
				# Email     
				Field(
					'email', 
					id="email-field", 
					css_class="emailfield",
					autocomplete='on',
					title=self.fields['email'].help_text,
					placeholder=_("Email"),
					wrapper_class='col-md-9'),

				# Location
				Field(
					"location",
					id="location-field",
					css_class="location_field", 
					autocomplete='on',
					title=self.fields['location'].help_text,
					placeholder=_("Location"),
					wrapper_class='col-md-9'),

				# Primary
				CustomCheckbox(
					"primary",
					title=self.fields['primary'].help_text),

				# Current
				CustomCheckbox(
					"current",
					title=self.fields['current'].help_text),

			),)

        # Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class TelephoneForm(BaseTelephone):
		
	def __init__(self, *args, **kwargs):
		super(TelephoneForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = Layout(
			
			# Fields
			Fieldset(
				(),
						
				# Number
				Field(
					'number', 
					id="number-field", 
					css_class="numberfield",
					autocomplete='on',
					title=self.fields['number'].help_text,
					placeholder=_("Number"),
					wrapper_class='col-md-9'),

				# Type
				Field(
					"type",
					id="type-field",
					css_class="type_field", 
					autocomplete='on',
					title=self.fields['type'].help_text,
					placeholder=_("Type"),
					wrapper_class='col-md-9'),

				# Primary
				CustomCheckbox(
					"primary",
					title=self.fields['primary'].help_text),

				# Current
				CustomCheckbox(
					"current",
					title=self.fields['current'].help_text),

			),)

        # Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class SocialForm(BaseSocial):
		
	def __init__(self, *args, **kwargs):
		super(SocialForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = Layout(
		
			# Fields
			Fieldset(
				(),
						
				# Service
				Field(
					'service', 
					id="service-field", 
					css_class="servicefield",
					autocomplete='on',
					title=self.fields['service'].help_text,
					placeholder=_("Service"),
					wrapper_class='col-md-9'),

				# Alias
				Field(
					"alias",
					id="alias-field",
					css_class="alias_field", 
					autocomplete='on',
					title=self.fields['alias'].help_text,
					placeholder=_("Alias"),
					wrapper_class='col-md-9'),

				# URL
				Field(
					"url",
					id="url-field",
					css_class="url_field", 
					autocomplete='on',
					title=self.fields['url'].help_text,
					placeholder=_("URL"),
					wrapper_class='col-md-9'),

				# Primary
				CustomCheckbox(
					"primary",
					title=self.fields['primary'].help_text),

				# Current
				CustomCheckbox(
					"current",
					title=self.fields['current'].help_text),

			),)

        # Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class WebsiteForm(BaseWebsite):
		
	def __init__(self, *args, **kwargs):
		super(WebsiteForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = Layout(

			# Fields
			Fieldset(
				(),

				# URL
				Field(
					"url",
					id="url-field",
					css_class="url_field", 
					autocomplete='on',
					title=self.fields['url'].help_text,
					placeholder=_("URL"),
					wrapper_class='col-md-9'),

				# Primary
				CustomCheckbox(
					"primary",
					title=self.fields['primary'].help_text),

				# Current
				CustomCheckbox(
					"current",
					title=self.fields['current'].help_text),

			),)

        # Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


# Person Forms
class BasePerson(forms.ModelForm):
	
	class Meta:
		model = Person
		fields = ['prefix', 'first_name', 'last_name', 'middle_names',
				'suffix', 'nickname', 'aliases',
				'gender', 'dob', 'height', 'weight', 'age',
				'description', 'taxfile', 'image_upload',
				'type', 'status', 'classification', 'category',
				'authorisation']


class PersonForm(BasePerson):
		
	def __init__(self, *args, **kwargs):
		super(PersonForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = Layout(
		   
			# Fields
			Fieldset(
				(),
				
				# Prefix
				Field(
					'prefix', 
					id="prefix-field", 
					css_class="prefixfield",
					autocomplete='on',
					title=self.fields['prefix'].help_text,
					placeholder=_("Prefix"),
					wrapper_class='col-md-9'),

				# First Name
				Field(
					'first_name', 
					id="first_name-field", 
					css_class="first_namefield",
					autocomplete='on',
					title=self.fields['first_name'].help_text,
					placeholder=_("First Name"),
					wrapper_class='col-md-9'),

				# Last Name
				Field(
					"last_name",
					id="last_name-field",
					css_class="last_name_field", 
					autocomplete='on',
					title=self.fields['last_name'].help_text,
					placeholder=_("Last Name"),
					wrapper_class='col-md-9'),

				# Middle Names
				Field(
					"middle_names",
					id="middle_names-field",
					css_class="middle_names_field", 
					autocomplete='on',
					title=self.fields['middle_names'].help_text,
					placeholder=_("Middle Names"),
					wrapper_class='col-md-9'),

				# Suffix
				Field(
					'suffix', 
					id="suffix-field", 
					css_class="suffixfield",
					autocomplete='on',
					title=self.fields['suffix'].help_text,
					placeholder=_("Suffix"),
					wrapper_class='col-md-9'),

				# Nickname
				Field(
					"nickname",
					id="nickname-field",
					css_class="nickname_field", 
					autocomplete='on',
					title=self.fields['nickname'].help_text,
					placeholder=_("Nickname"),
					wrapper_class='col-md-9'),
				
				# Aliases
				Field(
					"aliases",
					id="aliases-field",
					css_class="aliases_field", 
					autocomplete='on',
					title=self.fields['aliases'].help_text,
					placeholder=_("Aliases"),
					wrapper_class='col-md-9'),

				# Gender
				Field(
					'gender', 
					id="gender-field", 
					css_class="genderfield",
					autocomplete='on',
					title=self.fields['gender'].help_text,
					placeholder=_("Gender"),
					wrapper_class='col-md-9'),

				# Date Of Birth
				Field(
					"dob",
					id="dob-field",
					css_class="dob_field", 
					autocomplete='on',
					title=self.fields['dob'].help_text,
					placeholder=_("Date Of Birth"),
					wrapper_class='col-md-9'),

				# Height
				Field(
					"height",
					id="height-field",
					css_class="height_field", 
					autocomplete='on',
					title=self.fields['height'].help_text,
					placeholder=_("Height"),
					wrapper_class='col-md-9'),
				
				# Weight
				Field(
					'weight', 
					id="weight-field", 
					css_class="weightfield",
					autocomplete='on',
					title=self.fields['weight'].help_text,
					placeholder=_("Weight"),
					wrapper_class='col-md-9'),

				# Age
				Field(
					"age",
					id="age-field",
					css_class="age_field", 
					autocomplete='on',
					title=self.fields['age'].help_text,
					placeholder=_("Age"),
					wrapper_class='col-md-9'),

				# Description
				Field(
					"description",
					id="description-field",
					css_class="description_field", 
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Description"),
					wrapper_class='col-md-9'),

				# Taxfile
				Div(
					PrependedText(
						"taxfile", 
						_(""),
						id="taxfile-field",
						css_class="taxfilefield", 
						autocomplete='on',
						title=self.fields['taxfile'].help_text,
						placeholder=_("Taxfile"),
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

			),)
		
		# Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class PersonUpdateForm(PersonForm):
	
	change_reason = CharField(required=False, label='Reason For Change',)


# Company Forms
class BaseCompany(forms.ModelForm):
	
	class Meta:
		model = Company
		fields = ['title', 'code', 'logo_upload', 'industry', 'description',
				'type', 'status', 'classification', 'category', 'authorisation']


class CompanyForm(BaseCompany):
		
	def __init__(self, *args, **kwargs):
		super(CompanyForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = Layout(

			# Fields
			Fieldset(
				(),

				# Title
				Field(
					"title",
					id="title-field",
					css_class="title_field", 
					autocomplete='on',
					title=self.fields['title'].help_text,
					placeholder=_("Title"),
					wrapper_class='col-md-9'),

				# Code
				Field(
					"code",
					id="code-field",
					css_class="code_field", 
					autocomplete='on',
					title=self.fields['code'].help_text,
					placeholder=_("Code"),
					wrapper_class='col-md-9'),

				# Industry
				Field(
					"industry",
					id="industry-field",
					css_class="industry_field", 
					autocomplete='on',
					title=self.fields['industry'].help_text,
					placeholder=_("Industry"),
					wrapper_class='col-md-9'),
				
				# Description
				Field(
					"description",
					id="description-field",
					css_class="description_field", 
					autocomplete='on',
					title=self.fields['description'].help_text,
					placeholder=_("Description"),
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

				# Logo Upload
				Field(
					"logo_upload",
					id="logo_upload-field",
					css_class="logo_uploadfield", 
					autocomplete='on',
					title=self.fields['logo_upload'].help_text,
					placeholder=_("Logo Image Upload"),
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

			),)
		
		# Prevents help_text being shown outside of popovers
		for field in self.fields:
			self.fields[field].help_text = None


class CompanyUpdateForm(CompanyForm):
	
	change_reason = CharField(required=False, label='Reason For Change',)
