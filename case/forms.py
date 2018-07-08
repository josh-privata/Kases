"""
Case Forms.
"""

from django import forms
from case.models import Case
#, CaseTask, CaseNote
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, CharField, Textarea, Select, FileInput
from django.utils.text import slugify
import itertools
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from simple_history.utils import update_change_reason


class CrispyCaseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyCaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = layout.Layout(
            
            layout.Div(layout.Fieldset(_("Main data"),
                        layout.Field('title', wrapper_class='col-md-6'),
                        layout.Field('type', wrapper_class='col-md-6'),
                        layout.Field('status', wrapper_class='col-md-9'),
                        layout.Field('background', wrapper_class='col-md-3'),
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Main data"),
                          layout.Field("location", css_class="input-block-level"),
                          layout.Field("brief", css_class="input-block-level"),
                          layout.Field("description", css_class="input-blocklevel", rows="3"),
                          layout.Field("private"),
                          layout.Field("classification"),
                          layout.Div(bootstrap.PrependedText("reference", "", css_class="input-block-level"), css_id="contact_info",),),

            layout.Fieldset(_("Image"),
                          layout.Field("image_upload", css_class="input-block-level"),
                          layout.HTML(u"""{% load i18n %}
                            <p class="help-block">
                                {% trans "Available formats are JPG, GIF, and PNG. Minimal size is 800 × 800 px." %}
                            </p>"""),
                          title=_("Image upload"), css_id="image_fieldset",),

            layout.Fieldset(_("Authorisation"), 
                          layout.Field("authorisation"),
                          layout.Field("assigned_to"), 
                          layout.Field("manager"), 
                          layout.Div(bootstrap.PrependedText("reference", "", css_class="input-block-level", placeholder="contact@example.com"), css_id="contact_info",),),

            layout.Fieldset(_("Main data"),
                          bootstrap.Accordion(
                              bootstrap.AccordionGroup('First Group', layout.Field('brief', wrapper_class='card')),
                              bootstrap.AccordionGroup('Second Group', layout.Field('title', wrapper_class='card')),
                          ),),

            layout.Fieldset(_("Main data"),
                          bootstrap.TabHolder(
                            bootstrap.Tab('First Tab', layout.Field('location', wrapper_class='col-md-6')),
                            bootstrap.Tab('Second Tab',layout.Field('description', wrapper_class='col-md-6')),
                      ),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = Case
        fields = ['title', 'reference', 'background', 'purpose', 'location',
                 'description', 'brief', 'private', 'type', 'status',
                 'classification', 'priority', 'authorisation', 'image_upload', 'assigned_to',
                 'manager', 'assigned_by']

    def save(self):
        instance = super(CrispyCaseForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Case.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Case Creation')
        return instance


class CaseCreateForm(forms.ModelForm):

    title = CharField(max_length=200, required=False,)
    reference = CharField(max_length=200, required=False,)
    background = CharField(required=False,)
    location = CharField(max_length=200, required=False,)
    description = CharField(required=False,)
    brief = CharField(required=False,)
   
    class Meta:
        model = Case
        fields = ['title', 'reference', 'background', 'purpose', 'location',
                 'description', 'brief', 'private', 'assigned_to',
                 'manager', 'assigned_by']
        #'type', 'status', 'classification', 'priority', 'authorisation'
        labels = {
            'type': _('Case Type'),
            'title':_('Title'),
            'reference':_('Reference'),
            'background':_('Background'),
            'location':_('Location'),
            'description':_('Description'),
            'brief':_('Brief'),
        }
        error_messages = {
            'case': {'max_length': _("The Case Type is Invalid"),},
        }
        help_texts = {
            'title': _('Some useful help text.'),
        }
        widgets = {
            #'authorisation': Select(attrs={'class': 'form-control'}),
            #'priority': Select(attrs={'class': 'form-control'}),
            #'classification': Select(attrs={'class': 'form-control'}),
            #'status': Select(attrs={'class': 'form-control'}),
            #'type': Select(attrs={'class': 'form-control'}),
            #'assigned_by': Select(attrs={'class': 'form-control'}),
            #'assigned_to': Select(attrs={'class': 'form-control'}),
            #'manager': Select(attrs={'class': 'form-control'}),
            #'title': CharField(attrs={'max_length': 200, 'required': False}),
        }

    def save(self):
        instance = super(CaseCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Case.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Case Creation')
        return instance


class CaseEditForm(forms.ModelForm):

    change_reason = CharField(required=False, label='Reason For Change',)
    title = CharField(max_length=200, required=False,)
    reference = CharField(max_length=200, required=False,)
    background = CharField(required=False,)
    location = CharField(max_length=200, required=False,)
    description = CharField(required=False,)
    brief = CharField(required=False,)
   
    class Meta:
        model = Case
        fields = ['title', 'reference', 'background', 'purpose', 'location',
                 'description', 'brief', 'private', 'type', 'status',
                 'classification', 'priority', 'authorisation', 'image_upload', 'assigned_to',
                 'manager', 'assigned_by']
        labels = {
            'type': _('Case Type'),
            'title':_('Title'),
            'reference':_('Reference'),
            'background':_('Background'),
            'location':_('Location'),
            'description':_('Description'),
            'brief':_('Brief'),
        }
        error_messages = {
            'case': {'max_length': _("The Case Type is Invalid"),},
        }
        help_texts = {
            'title': _('Some useful help text.'),
        }
        widgets = {
            'authorisation': Select(attrs={'class': 'form-control'}),
            'priority': Select(attrs={'class': 'form-control'}),
            'classification': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'assigned_by': Select(attrs={'class': 'form-control'}),
            'assigned_to': Select(attrs={'class': 'form-control'}),
            'manager': Select(attrs={'class': 'form-control'}),
            'image_upload': FileInput(attrs={'class': 'form-control'}),
            #'title': CharField(attrs={'max_length': 200, 'required': False}),
        }

    def save(self):
        instance = super(CaseEditForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Case.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, 'Initial Case Creation')
        return instance

    
#class CaseNoteCreateForm(forms.ModelForm):
    
#    def __init__(self,*args,**kwargs):
#        self.case = kwargs.pop('case')
#        super(CaseNoteCreateForm,self).__init__(*args,**kwargs)
#        self.fields['case'].widget = forms.TextInput(attrs={'case': self.case})

#    title = CharField(max_length=200, required=False, label='Title',)
    
        
#    class Meta:
#        model = CaseNote
#        fields = ['title', 'slug', 'image_upload', 'private', 'type', 'status', 'classification', 'priority', 'category', 'authorisation', 'assigned_to', 'manager', 'assigned_by', 'description', 'case']

#    def save(self):
#        instance = super(CaseNoteCreateForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not CaseNote.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        instance.case = self.case
#        #changereason = self.cleaned_data['change_reason']
#        instance.save()
#        #update_change_reason(instance, changereason)
#        return instance


#class CaseTaskCreateForm(forms.ModelForm):

#    title = CharField(max_length=200, required=False, label='Title',)
#    background = CharField(required=False, label='Background',)
#    location = CharField(max_length=200, required=False, label='Location',)
#    description = CharField(required=False, label='Description',)
#    change_reason = CharField(required=False, label='Reason For Change',)

#    class Meta:
#        model = CaseTask
#        fields = ['title', 'background', 'location', 'description', 'private', 'type', 'status', 'priority', 'authorisation',]

#    def save(self):
#        instance = super(CaseTaskForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not CaseTask.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        changereason = self.cleaned_data['change_reason']
#        instance.save()
#        update_change_reason(instance, changereason)
#        return instance


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
#                  recipient_list=[cleaned_data["recipient"].email],
#                  fail_silently=True,)