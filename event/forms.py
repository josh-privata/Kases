"""
Event Forms.
"""


from django import forms
from event.models import Event
#, EventEvent, EventTask
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, CharField, Textarea, Select, FileInput
from django.utils.text import slugify
import itertools
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from simple_history.utils import update_change_reason


#'title', 'slug', 'image_upload', 'private', 'type', 'status',
#'classification', 'priority', 'category', 'authorisation', 'assigned_to',
#'manager', 'assigned_by', 'description'


#class EventForm(forms.ModelForm):

#    class Meta:
#        model = Event
#        fields = ['title', 'slug', 'image_upload', 'private', 'type', 'status',
#                  'classification', 'priority', 'category', 'authorisation', 'assigned_to',
#                  'manager', 'assigned_by', 'description']


class CrispyEventForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CrispyEventForm, self).__init__(*args, **kwargs)
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
                        #css_class='form-row'
                        )),

            layout.Fieldset(_("Main data"),
                          layout.Field("classification"),),

            layout.Fieldset(_("Main data"),
                          bootstrap.TabHolder(
                            bootstrap.Tab('Second Tab',layout.Field('description', wrapper_class='col-md-6')),
                      ),),

            bootstrap.FormActions(layout.Submit("submit", _("Save")),))

    class Meta:
        model = Event
        fields = ['title', 'slug', 'image_upload', 'private', 'type', 'status',
                  'classification', 'priority', 'category', 'authorisation', 'assigned_to',
                  'manager', 'assigned_by', 'description']

    def save(self):
        instance = super(CrispyEventForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Event.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Event Creation')
        return instance


class EventCreateForm(forms.ModelForm):

    title = CharField(max_length=200, required=False,)
    reference = CharField(max_length=200, required=False,)
    description = CharField(required=False,)
   
    class Meta:
        model = Event
        fields = ['title', 'slug', 'image_upload', 'private', 'type', 'status',
                  'classification', 'priority', 'category', 'authorisation', 'assigned_to',
                  'manager', 'assigned_by', 'description']
        labels = {
            'type': _('Event Type'),
            'title':_('Title'),
            'description':_('Description'),
        }
        error_messages = {
            'event': {'max_length': _("The Event Type is Invalid"),},
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
        instance = super(EventCreateForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Event.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        instance.save()
        update_change_reason(instance, 'Initial Event Creation')
        return instance


class EventEditForm(forms.ModelForm):

    change_reason = CharField(required=False, label='Reason For Change',)
    title = CharField(max_length=200, required=False,)
    description = CharField(required=False,)
   
    class Meta:
        model = Event
        fields = ['title', 'slug', 'image_upload', 'private', 'type', 'status',
                  'classification', 'priority', 'category', 'authorisation', 'assigned_to',
                  'manager', 'assigned_by', 'description']
        labels = {
            'type': _('Event Type'),
            'title':_('Title'),
            'description':_('Description'),
        }
        error_messages = {
            'event': {'max_length': _("The Event Type is Invalid"),},
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
        instance = super(EventEditForm, self).save(commit=False)
        instance.slug = orig = slugify(instance.title)
        for x in itertools.count(1):
            if not Event.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)
        changereason = self.cleaned_data['change_reason']
        instance.save()
        update_change_reason(instance, 'Initial Event Creation')
        return instance