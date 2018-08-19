## Entity Forms ##

from django import forms
from simple_history.models import HistoricalRecords
from crispy_forms.layout import *
from entity.models.person import Person
from entity.models.entity import Address, Telephone, Email, Website, Social, Country, State, Note
from entity.models.company import Company
#import vobject

# Person
#'prefix', 'first_name', 'last_name', 'middle_names', 'suffix', 'nickname', 'aliases',
#'notes', 'gender', 'birthday', 'anniversary', 'height', 'weight', 'age', 'taxfile',
#'date_started', 'salary', 'job_title', 'role', '#company', '#social', 'address',
#'telephone', 'email', 'website', 'type', 'status', 'classification', 'category', 'authorisation'

# Company
#'title', 'code', '#image', 'primary_market', 'industry', '#social', 'address',
#'telephone', 'email', 'website', 'type', 'status', 'classification', 'category', 'authorisation'

# Address
#'line1', 'line2', 'line3', 'city', '#state', 'postcode'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('text',)


class TelephoneForm(forms.ModelForm):
    class Meta:
        model = Telephone
        fields = '__all__'


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'


class SocialForm(forms.ModelForm):
    class Meta:
        model = Social
        fields = '__all__'


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = '__all__'


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('address','telephone','email','website','social','created','modified')


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('address','telephone','email','website','social','created','modified')
        

class SearchForm(forms.Form):
    first = forms.CharField(required=False,help_text="First Name")
    last = forms.CharField(required=False,help_text="Last Name")
    
    
class AdvancedSearchForm(forms.Form):
    first = forms.CharField(required=False)
    last = forms.CharField(required=False)
    line1 = forms.CharField(label="Address Line 1",required=False)
    line2 = forms.CharField(label="Address Line 2",required=False)
    line3 = forms.CharField(label="Address Line 3",required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    postcode = forms.CharField(required=False)
    country = forms.ChoiceField(choices=[('','--------')]+list(Country.objects.order_by('title').values_list('code','title')),required=False)
    phone = forms.CharField(label='Telephone Number',required=False)
    has_phone = forms.BooleanField(label='Has a telephone number?', required=False)
    email = forms.CharField(label='Email Address',required=False)
    website = forms.CharField(label='Website',required=False)
    

class ExportForm(forms.Form):

    ids = forms.CharField(required=True,help_text="Primary keys", widget=forms.HiddenInput)