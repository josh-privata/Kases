## Entity Forms ##
from django.forms import CharField, Select, FileInput, modelformset_factory
from django import forms
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _
from crispy_forms import bootstrap, layout
from simple_history.utils import update_change_reason
from crispy_forms.helper import FormHelper
from entity.models.person import Person
from entity.models.entity import Address, Telephone, Email, Website, Social, Country, State, Note
from entity.models.company import Company
#import vobject

# Person
#'prefix', 'first_name', 'last_name', 'middle_names', 'suffix', 'nickname','aliases',
#'gender', 'birthday', 'anniversary', 'height', 'weight', 'age',
#'taxfile', 'date_started', 'salary', 'job_title', 'role', 'company',
#'type', 'status', 'classification', 'category', 'authorisation'
##'address', 'telephone', 'email', 'website', 'social''

# Company
#'title', 'code', '#image', 'notes', 'primary_market', 'industry', 'prefix'
# 'type', 'status', 'classification', 'category', 'authorisation'
## 'social', 'address', 'telephone', 'email', 'website',

# Address
#'line1', 'line2', 'line3', 'city', '#state', 'postcode', 'type', 'location', 'primary'

# Note
# 'text', 'author', 'added'

# Telephone
# 'number', 'type', 'location', 'primary'

# Email
# 'email', 'location', 'primary'

# Social
#'service', 'alias', 'url', 'location', 'primary'

# Website
# 'url', 'location', 'primary'

class Old_AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class Old_NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('text',)


class Old_TelephoneForm(forms.ModelForm):
    class Meta:
        model = Telephone
        fields = '__all__'

        
class Old_EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'


class Old_SocialForm(forms.ModelForm):
    class Meta:
        model = Social
        fields = '__all__'


class Old_WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = '__all__'


class Old_PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('address','telephone','email','website','social','created','modified')


class Old_CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('address','telephone','email','website','social','created','modified')


class NoteForm(forms.ModelForm):
    	
	def __init__(self, *args, **kwargs):
		super(NoteForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = layout.Layout(
						  layout.Fieldset(_("Main data"),
						  layout.Field("text", css_class="input-block-level"),
						  layout.Field("author", css_class="input-block-level"),
						  layout.Field("added", css_class="input-blocklevel"),),)

	class Meta:
		model = Note
		fields = ['text', 'author', 'added']


class AddressForm(forms.ModelForm):
    	
	def __init__(self, *args, **kwargs):
		super(AddressForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = layout.Layout(
						  layout.Fieldset(""),
						  layout.Field("line1", css_class="input-block-level"),
						  layout.Field("line2", css_class="input-block-level"),
						  layout.Field("line3", css_class="input-blocklevel"),
                          layout.Field("city", css_class="input-blocklevel"),
                          layout.Field("postcode", css_class="input-blocklevel"),
                          layout.Field("location", css_class="input-blocklevel"),
                          layout.Field("primary", css_class="input-blocklevel"),
                          layout.Field("type", css_class="input-blocklevel"),)

	class Meta:
		model = Address
		fields = ['line1', 'line2', 'line3', 'city', 'postcode', 'type', 'location', 'primary']


class EmailForm(forms.ModelForm):
    	
	def __init__(self, *args, **kwargs):
		super(EmailForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = layout.Layout(
						  layout.Fieldset(_("Email"),
						  layout.Field("email", css_class="input-block-level"),
                          layout.Field("location", css_class="input-blocklevel"),
                          layout.Field("primary", css_class="input-blocklevel"),),)

	class Meta:
		model = Email
		fields = ['email', 'location', 'primary']


class TelephoneForm(forms.ModelForm):
    	
	def __init__(self, *args, **kwargs):
		super(TelephoneForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = layout.Layout(
						  layout.Fieldset(_("Phone Numbers"),
						  layout.Field("number", css_class="input-block-level"),
						  layout.Field("type", css_class="input-blocklevel"),
                          layout.Field("location", css_class="input-blocklevel"),
                          layout.Field("primary", css_class="input-blocklevel"),),)

	class Meta:
		model = Telephone
		fields = ['number', 'type', 'location', 'primary']


class SocialForm(forms.ModelForm):
    	
	def __init__(self, *args, **kwargs):
		super(SocialForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = layout.Layout(
						  layout.Fieldset(_("Social Media"),
						  layout.Field("number", css_class="input-block-level"),
						  layout.Field("type", css_class="input-blocklevel"),
                          layout.Field("location", css_class="input-blocklevel"),
                          layout.Field("primary", css_class="input-blocklevel"),),)

	class Meta:
		model = Social
		fields = ['service', 'alias', 'url', 'location', 'primary']


class WebsiteForm(forms.ModelForm):
    	
	def __init__(self, *args, **kwargs):
		super(WebsiteForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = layout.Layout(
						  layout.Fieldset(_("Websites"),
						  layout.Field("url", css_class="input-block-level"),
                          layout.Field("location", css_class="input-blocklevel"),
                          layout.Field("primary", css_class="input-blocklevel"),),)

	class Meta:
		model = Website
		fields = ['url', 'location', 'primary']


class PersonForm(forms.ModelForm):
    	
	def __init__(self, *args, **kwargs):
		super(PersonForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = layout.Layout(

						  layout.Fieldset(_("General"),
                          layout.Field('change_reason', css_class="input-block-level"),
						  layout.Field("prefix", css_class="input-block-level"),
						  layout.Field("first_name", css_class="input-block-level"),
						  layout.Field("middle_names", css_class="input-blocklevel"),
                          layout.Field("last_name", css_class="input-blocklevel"),
                          layout.Field("suffix", css_class="input-blocklevel"),
                          layout.Field("nickname", css_class="input-blocklevel"),
                          layout.Field("aliases", css_class="input-blocklevel"),),
                          
                          layout.Fieldset(_("Personal"),
						  layout.Field("gender", css_class="input-block-level"),
						  layout.Field("birthday", css_class="input-block-level"),
						  layout.Field("anniversary", css_class="input-blocklevel"),
                          layout.Field("height", css_class="input-blocklevel"),
                          layout.Field("weight", css_class="input-blocklevel"),
                          layout.Field("age", css_class="input-blocklevel"),),
                          
                          layout.Fieldset(_("Work"),
						  layout.Field("taxfile", css_class="input-block-level"),
						  layout.Field("date_started", css_class="input-block-level"),
						  layout.Field("salary", css_class="input-blocklevel"),
                          layout.Field("job_title", css_class="input-blocklevel"),
                          layout.Field("role", css_class="input-blocklevel"),),

                          layout.Fieldset(_("Other"),
						  layout.Field("type", css_class="input-block-level"),
						  layout.Field("status", css_class="input-block-level"),
						  layout.Field("classification", css_class="input-blocklevel"),
                          layout.Field("category", css_class="input-blocklevel"),
                          layout.Field("authorisation", css_class="input-blocklevel"),)

                          ,)

	class Meta:
		model = Person
		fields = ['prefix', 'first_name', 'last_name', 'middle_names', 'suffix', 'nickname',
                'aliases', 'gender', 'birthday', 'anniversary', 'height', 'weight', 'age',
                'taxfile', 'date_started', 'salary', 'job_title', 'role',
                'type', 'status', 'classification', 'category', 'authorisation']


class PersonUpdateForm(PersonForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(PersonUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        self.save_m2m()
        return instance


class CompanyForm(forms.ModelForm):
    	
	def __init__(self, *args, **kwargs):
		super(CompanyForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.layout = layout.Layout(

						  layout.Fieldset(_("General"),
                          layout.Field('change_reason', css_class="input-block-level"),
						  layout.Field("title", css_class="input-block-level"),
						  layout.Field("code", css_class="input-block-level"),
						  layout.Field("notes", css_class="input-blocklevel"),
                          layout.Field("primary_market", css_class="input-blocklevel"),
                          layout.Field("industry", css_class="input-blocklevel"),),
                          
                          layout.Fieldset(_("Other"),
						  layout.Field("type", css_class="input-block-level"),
						  layout.Field("status", css_class="input-block-level"),
						  layout.Field("classification", css_class="input-blocklevel"),
                          layout.Field("category", css_class="input-blocklevel"),
                          layout.Field("authorisation", css_class="input-blocklevel"),)

                          ,)

	class Meta:
		model = Company
		fields = ['title', 'code', 'notes', 'primary_market', 'industry', 
                 'type', 'status', 'classification', 'category', 'authorisation']


class CompanyUpdateForm(CompanyForm):
    
    change_reason = CharField(required=False, label='Reason For Change',)

    def save(self):
        instance = super(CompanyUpdateForm, self).save(commit=False)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, changereason)
        self.save_m2m()
        return instance


class SearchForm(forms.Form):
    first = forms.CharField(required=False,help_text="First Name")
    last = forms.CharField(required=False,help_text="Last Name")
    
    
class AdvancedSearchForm(forms.Form):
    pass
    

class ExportForm(forms.Form):
    pass