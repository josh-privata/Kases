from django import forms
from django.contrib.auth.models import User
from user.models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'prefix', 'suffix', 'nickname', 'aliases',
                    'notes', 'gender', 'age', 'taxfile',
                    'date_started', 'job_title', 'role', 'status',
                    'classification', 'authorisation')


#class CrispyUserForm(forms.ModelForm):
#	def __init__(self, *args, **kwargs):
#		super(CrispyUserForm, self).__init__(*args, **kwargs)
#		self.helper = FormHelper()
#		self.helper.form_action = ""
#		self.helper.form_method = "POST"
#		self.helper.form_class = 'form-horizontal'
#		self.helper.label_class = 'col-lg-2'
#		self.helper.field_class = 'col-lg-8'
#		self.helper.layout = layout.Layout(
    #			
#			layout.Div(layout.Fieldset(_("Main data"),
#						layout.Field('title', wrapper_class='col-md-9'),
#						)),

#			layout.Fieldset(_("Main data"),
#						  layout.Div(bootstrap.PrependedText("status", "", css_class="input-block-level"), css_id="contact_info",),
#						  layout.Div(bootstrap.PrependedText("classification", "", css_class="input-block-level"), css_id="contact_info",),
#						  layout.Div(bootstrap.PrependedText("priority", "", css_class="input-block-level"), css_id="contact_info",),
#						  layout.Div(bootstrap.PrependedText("category", "", css_class="input-block-level"), css_id="contact_info",),
#						  layout.Div(bootstrap.PrependedText("authorisation", "", css_class="input-block-level"), css_id="contact_info",),
#                          ),

#			layout.Fieldset(_("Authorisation"), 
#						  layout.Field("assigned_by"),
#						  layout.Field("assigned_to"), 
#						  layout.Field("managed_by"),),

#			bootstrap.FormActions(layout.Submit("submit", _("Save")),))

#	class Meta:
#		model = Case
#		fields = ['title', 'reference', 'background', 'purpose', 'location', 'brief',
#				  'image_upload',
#				  'type', 'status', 'classification', 'priority', 'category',
#				  'authorisation', 'assigned_to', 'managed_by', 'assigned_by',
#				  'description', 'private']
