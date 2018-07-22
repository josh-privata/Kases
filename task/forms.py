"""
Task Forms.
"""

from django import forms
from task.models import Task
#, TaskTask
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, CharField, Textarea, Select, FileInput
from django.utils.text import slugify
import itertools
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from simple_history.utils import update_change_reason


#class CrispyTaskForm(forms.ModelForm):
    
#    def __init__(self, *args, **kwargs):
#        super(CrispyTaskForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_action = ""
#        self.helper.form_method = "POST"
#        self.helper.form_class = 'form-horizontal'
#        self.helper.label_class = 'col-lg-2'
#        self.helper.field_class = 'col-lg-8'
#        self.helper.layout = layout.Layout(
            
#            layout.Div(layout.Fieldset(_("Main data"),
#                        layout.Field('title', wrapper_class='col-md-6'),
#                        layout.Field('type', wrapper_class='col-md-6'),
#                        layout.Field('status', wrapper_class='col-md-9'),
#                        layout.Field('background', wrapper_class='col-md-3'),
#                        #css_class='form-row'
#                        ),),

#            layout.Fieldset(_("Main data"),
#                          layout.Field("location", css_class="input-block-level"),
#                          layout.Field("description", css_class="input-blocklevel", rows="3"),
#                          layout.Field("private"),
#                          layout.Field("classification"),),

#            layout.Fieldset(_("Authorisation"), 
#                          layout.Field("authorisation"),
#                          layout.Field("assigned_to"), 
#                          layout.Field("manager"),), 

#            layout.Fieldset(_("Main data"),
#                          bootstrap.Accordion(
#                              bootstrap.AccordionGroup('First Group', layout.Field('brief', wrapper_class='card')),
#                          ),),

#            layout.Fieldset(_("Main data"),
#                          bootstrap.TabHolder(
#                            bootstrap.Tab('First Tab', layout.Field('location', wrapper_class='col-md-6')),
#                            bootstrap.Tab('Second Tab',layout.Field('description', wrapper_class='col-md-6')),
#                      ),),

#            bootstrap.FormActions(layout.Submit("submit", _("Save")),),)

#    class Meta:
#        model = Task
#        fields = ['title', 'background', 'description', 'location', 'type', 'status', 'classification', 'priority', 'authorisation',
#                  'category', 'assigned_to', 'assigned_by']

#    def save(self):
#        instance = super(CrispyTaskForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not Task.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        instance.save()
#        update_change_reason(instance, 'Initial Task Creation')
#        return instance


#class TaskCreateForm(forms.ModelForm):

#    title = CharField(max_length=200, required=False,)
#    reference = CharField(max_length=200, required=False,)
#    background = CharField(required=False,)
#    location = CharField(max_length=200, required=False,)
#    description = CharField(required=False,)
   
#    class Meta:
#        model = Task
#        fields = ['title', 'background', 'description', 'reference', 'location', 'type', 'status', 'classification', 'priority', 'authorisation',
#                  'category', 'assigned_to', 'assigned_by']
#        #'type', 'status', 'classification', 'priority', 'authorisation'
#        labels = {
#            'type': _('Task Type'),
#            'title':_('Title'),
#            'reference':_('Reference'),
#            'background':_('Background'),
#            'location':_('Location'),
#            'description':_('Description'),
#        }
#        error_messages = {
#            'task': {'max_length': _("The Task Type is Invalid"),},
#        }
#        help_texts = {
#            'title': _('Some useful help text.'),
#        }
#        widgets = {
#            #'authorisation': Select(attrs={'class': 'form-control'}),
#            #'priority': Select(attrs={'class': 'form-control'}),
#            #'classification': Select(attrs={'class': 'form-control'}),
#            #'status': Select(attrs={'class': 'form-control'}),
#            #'type': Select(attrs={'class': 'form-control'}),
#            #'assigned_by': Select(attrs={'class': 'form-control'}),
#            #'assigned_to': Select(attrs={'class': 'form-control'}),
#            #'manager': Select(attrs={'class': 'form-control'}),
#            #'title': CharField(attrs={'max_length': 200, 'required': False}),
#        }

#    def save(self):
#        instance = super(TaskCreateForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not Task.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        instance.save()
#        update_change_reason(instance, 'Initial Task Creation')
#        return instance


#class TaskEditForm(forms.ModelForm):

#    change_reason = CharField(required=False, label='Reason For Change',)
#    title = CharField(max_length=200, required=False,)
#    reference = CharField(max_length=200, required=False,)
#    background = CharField(required=False,)
#    location = CharField(max_length=200, required=False,)
#    description = CharField(required=False,)
   
#    class Meta:
#        model = Task
#        fields = ['title', 'background', 'description', 'reference', 'location', 'type', 'status', 'classification', 'priority', 'authorisation',
#                  'category', 'assigned_to', 'assigned_by']
#        labels = {
#            'type': _('Task Type'),
#            'title':_('Title'),
#            'reference':_('Reference'),
#            'background':_('Background'),
#            'location':_('Location'),
#            'description':_('Description'),
#        }
#        error_messages = {
#            'task': {'max_length': _("The Task Type is Invalid"),},
#        }
#        help_texts = {
#            'title': _('Some useful help text.'),
#        }
#        widgets = {
#            'authorisation': Select(attrs={'class': 'form-control'}),
#            'priority': Select(attrs={'class': 'form-control'}),
#            'classification': Select(attrs={'class': 'form-control'}),
#            'status': Select(attrs={'class': 'form-control'}),
#            'type': Select(attrs={'class': 'form-control'}),
#            'assigned_by': Select(attrs={'class': 'form-control'}),
#            'assigned_to': Select(attrs={'class': 'form-control'}),
#            'manager': Select(attrs={'class': 'form-control'}),
#            #'title': CharField(attrs={'max_length': 200, 'required': False}),
#        }

#    def save(self):
#        instance = super(TaskEditForm, self).save(commit=False)
#        instance.slug = orig = slugify(instance.title)
#        for x in itertools.count(1):
#            if not Task.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#        changereason = self.cleaned_data['change_reason']
#        instance.save()
#        update_change_reason(instance, 'Initial Task Creation')
#        return instance

    
##class TaskNoteCreateForm(forms.ModelForm):
    
##    def __init__(self,*args,**kwargs):
##        self.task = kwargs.pop('task')
##        super(TaskNoteCreateForm,self).__init__(*args,**kwargs)
##        self.fields['task'].widget = forms.TextInput(attrs={'task': self.task})

##    title = CharField(max_length=200, required=False, label='Title',)
    
        
##    class Meta:
##        model = TaskNote
##        fields = ['title', 'slug', 'image_upload', 'private', 'type', 'status', 'classification', 'priority', 'category', 'authorisation', 'assigned_to', 'manager', 'assigned_by', 'description', 'task']

##    def save(self):
##        instance = super(TaskNoteCreateForm, self).save(commit=False)
##        instance.slug = orig = slugify(instance.title)
##        for x in itertools.count(1):
##            if not TaskNote.objects.filter(slug=instance.slug).exists():
##                break
##            instance.slug = '%s-%d' % (orig, x)
##        instance.task = self.task
##        #changereason = self.cleaned_data['change_reason']
##        instance.save()
##        #update_change_reason(instance, changereason)
##        return instance


##class TaskTaskCreateForm(forms.ModelForm):

##    title = CharField(max_length=200, required=False, label='Title',)
##    background = CharField(required=False, label='Background',)
##    location = CharField(max_length=200, required=False, label='Location',)
##    description = CharField(required=False, label='Description',)
##    change_reason = CharField(required=False, label='Reason For Change',)

##    class Meta:
##        model = TaskTask
##        fields = ['title', 'background', 'location', 'description', 'private', 'type', 'status', 'priority', 'authorisation',]

##    def save(self):
##        instance = super(TaskTaskForm, self).save(commit=False)
##        instance.slug = orig = slugify(instance.title)
##        for x in itertools.count(1):
##            if not TaskTask.objects.filter(slug=instance.slug).exists():
##                break
##            instance.slug = '%s-%d' % (orig, x)
##        changereason = self.cleaned_data['change_reason']
##        instance.save()
##        update_change_reason(instance, changereason)
##        return instance


##class MessageForm(forms.Form):
##    recipient = forms.ModelChoiceField(label=_("Recipient"), queryset=User.objects.all(), required=True,)
##    message = forms.CharField(label=_("Message"), widget=forms.Textarea, required=True,)

##    def __init__(self, request, *args, **kwargs):
##        super(MessageForm, self).__init__(*args, **kwargs)
##        self.request = request
##        self.fields["recipient"].queryset = self.fields["recipient"].queryset.exclude(pk=request.user.pk)


##    def save(self):
##        cleaned_data = self.cleaned_data
##        send_mail(subject=ugettext("A message from %s") % self.request.user,
##                  message=cleaned_data["message"],
##                  from_email=self.request.user.email,
##                  recipient_list=[cleaned_data["recipient"].email],
##                  fail_silently=True,)