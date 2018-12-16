"""
Definition of forms.
"""

import itertools
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from simple_history.utils import update_change_reason
from utils.models import Note

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class CrispyNoteForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyNoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('note', wrapper_class='col-md-6'),
                        layout.Field('private', wrapper_class='col-md-6'),
                        )),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = Note
        fields = ['note', 'private']

    def save(self):
        instance = super(CrispyNoteForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Note.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Note Creation')
        return instance