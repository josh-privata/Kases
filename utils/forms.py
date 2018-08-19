"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

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


#class MessageForm(forms.Form):
#    recipient = forms.ModelChoiceField(label=_("Recipient"), queryset=User.objects.all(), required=True,)
#    message = forms.CharField(label=_("Message"), widget=forms.Textarea, required=True,)

#    def __init__(self, request, *args, **kwargs):
#        super(MessageForm, self).__init__(*args, **kwargs)
#        self.request = request
#        self.fields["recipient"].queryset = self.fields["recipient"].queryset.exclude(pk=request.user.pk)

#    def save(self):
#        cleaned_data = self.cleaned_data
#        send_mail(subject=ugettext("A message from %s") % self.request.user,
#                  message=cleaned_data["message"],
#                  from_email=self.request.user.email,
#                  recipient_list=[cleaned_data["recipient"].email], fail_silently=True,)
