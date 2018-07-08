## Case Models ##

## python imports
from django.db import models
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#import case.managers as managers
from simple_history.models import HistoricalRecords
from note.models import Note
from task.models import Task


## Admin Models
class CaseAuthorisation(Authorisation):
    # General Fields

    class Meta:
        verbose_name = _('Case Classification')
        verbose_name_plural = _('Case Classifications')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    

class CaseClassification(Classification):
    # General Fields
    
    class Meta:
        verbose_name = _('Case Classification')
        verbose_name_plural = _('Case Classifications')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CaseType(Type):
    # General Fields
    
    class Meta:
        verbose_name = _('Case Type')
        verbose_name_plural = _('Case Types')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CasePriority(Priority):
    # General Fields
   
    class Meta:
        verbose_name = _('Case Priority')
        verbose_name_plural = _('Case Priorities')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CaseCategory(Category):
    # General Fields
    
    class Meta:
        verbose_name = _('Case Category')
        verbose_name_plural = _('Case Categories')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CaseStatus(Status):
    # General Fields

    class Meta:
        verbose_name = _('Case Status')
        verbose_name_plural = _('Case Status')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CaseStatusGroup(StatusGroup):
    ## Choices
    # CREATED = 'Created'
    # PENDING = 'Awaiting Authorisation'
    # REJECTED = 'Rejected'
    # OPEN = 'Open'
    # Active = 'Active'
    # CLOSED = 'Closed'
    # ARCHIVED = 'Archived'
    ## Choice Groups
    # closedStatuses = [CLOSED, ARCHIVED]
    # all_statuses = [CREATED, OPEN, CLOSED, ARCHIVED, PENDING, REJECTED]
    # approved_statuses = [CREATED, OPEN, CLOSED, ARCHIVED]
    # active_statuses = [CREATED, PENDING, REJECTED, OPEN]
    # workable_statuses = [CREATED, OPEN]
    # forensic_statuses = [OPEN]
    
    # General Fields
    # Linked Fields
    status = models.ManyToManyField(CaseStatus, blank=True, verbose_name="Case Status")

    class Meta:
        verbose_name = _('Case Status Group')
        verbose_name_plural = _('Case Status Groups')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


## Main Models
class Case(ObjectDescriptionMixin):
    # General Fields
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Title")
    #description= models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Description")
    reference = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Reference")
    background = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Background")
    purpose = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Purpose")
    location = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Location")
    brief = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Brief")
    private = models.BooleanField(default=False, blank=True, verbose_name="Private")
    slug = models.SlugField(blank=True, null=True, unique=True, verbose_name="Case Slug")
    image_upload = models.FileField(blank=True, null=True, verbose_name="Case Image")

    # Linked Fields
    type = models.ForeignKey(CaseType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Type")
    status = models.ForeignKey(CaseStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Status")
    classification = models.ForeignKey(CaseClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Classification")
    priority = models.ForeignKey(CasePriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Priority")
    category = models.ForeignKey(CaseCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Category")
    authorisation = models.ForeignKey(CaseAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Authorisation")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='case_assigned_to', blank=True, verbose_name="Assigned To")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_manager', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Case Manager")
    #legal = models.ManyToManyField(Personality, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Legal Advisor")
    #client = models.ManyToManyField(Personality, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Client")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")
    
    # Auto Fields
    date_added = models.DateTimeField(auto_now=True, null=True, verbose_name="Date Added")
    deadline = models.DateTimeField(auto_now=True, null=True, verbose_name="Deadline")

    history = HistoricalRecords()
    #manager = managers.CaseManager()

    class Meta:
        ordering = ('id',)
        verbose_name = _('Case')
        verbose_name_plural = _('Cases')

    def get_absolute_url(self):
        return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    
    
    # Property Methods
    def _get_case(self):
        """ A user-friendly Case ID, which is a combination of Case ID and queue slug. This is generally used in e-mail subjects. """
        return u"[%s]" % self.case_for_url
    case = property(_get_case)

    def _get_case_for_url(self):
        """ A URL-friendly Case ID, used in links. """
        return u"%s-%s" % (self.queue.slug, self.id)
    case_for_url = property(_get_case_for_url)  
    
    def _get_assigned_to(self):
        """
        Custom property to allow us to easily print 'Unassigned' if a Case has no owner, or the users name if it's assigned.
        If the user has a full name configured, we use that, otherwise their username.
        """
        if not self.assigned_to:
            return _('Unassigned')
        else:
            if self.assigned_to.get_full_name():
                return self.assigned_to.get_full_name()
            else:
                return self.assigned_to.get_username()
    get_assigned_to = property(_get_assigned_to)


## Data Models
class LinkedCase(ObjectDescriptionMixin):
    # General Fields
    reason = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Reason For Link")
    date_time = models.DateTimeField(auto_now=True, null=True, verbose_name="Date")
    # Linked Fields
    linked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="the")
    case = models.ManyToManyField(Case, blank=True, verbose_name="Case")


#class CaseTask(Task):
#    # Linked Fields
#    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")


#class CaseNote(Note):
#    # Linked Fields
#    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")


class CaseLog(ObjectDescriptionMixin):
    # General Fields
    entry = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Log Entry")
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")

    def __str__(self):
        return '%s' % self.entry


class CaseContact(ObjectDescriptionMixin):
    # General Fields
    reason = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Reason for Association")
    # Linked Fields
    #contact = models.ForeignKey(Personality, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Contact")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Case")

    class Meta:
        ordering = ('id',)
        verbose_name = _('Case Contact')
        verbose_name_plural = _('Case Contacts')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title