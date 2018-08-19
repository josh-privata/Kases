## Event Models ##

## python imports
from django.db import models
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#import event.managers as managers
from simple_history.models import HistoricalRecords


## Admin Models
class EventAuthorisation(Authorisation):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Authorisation')
        verbose_name_plural = _('Event Authorisations')

    #def get_absolute_url(self):
    #    return reverse('Event_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    

class EventClassification(Classification):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Classification')
        verbose_name_plural = _('Event Classifications')

    #def get_absolute_url(self):
    #    return reverse('Event_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EventType(Type):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Type')
        verbose_name_plural = _('Event Types')

    #def get_absolute_url(self):
    #    return reverse('Event_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EventPriority(Priority):
    # General Fields
   
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Priority')
        verbose_name_plural = _('Event Priorities')

    #def get_absolute_url(self):
    #    return reverse('Event_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EventCategory(Category):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Category')
        verbose_name_plural = _('Event Categories')

    #def get_absolute_url(self):
    #    return reverse('event_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EventStatus(Status):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Status')
        verbose_name_plural = _('Event Status')

    #def get_absolute_url(self):
    #    return reverse('Event_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EventStatusGroup(StatusGroup):
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
    status = models.ManyToManyField(EventStatus, blank=True, verbose_name="Event Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Status Group')
        verbose_name_plural = _('Event Status Groups')

    #def get_absolute_url(self):
    #    return reverse('Event_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


## Main Models
class Event(ObjectDescriptionMixin):
    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Event Title")
    slug = models.SlugField(blank=True, null=True, unique=True, verbose_name="Event Slug")
    image_upload = models.FileField(blank=True, null=True, verbose_name="Event Image")
    #deadline = models.DateTimeField(auto_now=False, null=True, verbose_name="Deadline")
    brief = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Brief")

    # Linked Fields
    type = models.ForeignKey(EventType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Event Type")
    status = models.ForeignKey(EventStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Event Status")
    classification = models.ForeignKey(EventClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Event Classification")
    priority = models.ForeignKey(EventPriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Event Priority")
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Event Category")
    authorisation = models.ForeignKey(EventAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Event Authorisation")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_assigned_to', blank=True, verbose_name="Assigned To")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='event_manager', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Event Manager")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='event_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")
    
    # Auto Fields

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.title


## Data Models