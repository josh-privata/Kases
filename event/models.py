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
    """
    Inherited model to contain information about an event authorisation.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Authorisation')
        verbose_name_plural = _('Event Authorisations')
    

class EventClassification(Classification):
    """
    Inherited model to contain information about an event classification.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Classification')
        verbose_name_plural = _('Event Classifications')


class EventType(Type):
    """
    Inherited model to contain information about an event type.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Type')
        verbose_name_plural = _('Event Types')


class EventPriority(Priority):
    """
    Inherited model to contain information about an event priority.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """
   
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Priority')
        verbose_name_plural = _('Event Priorities')


class EventCategory(Category):
    """
    Inherited model to contain information about an event category.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    
    """
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Category')
        verbose_name_plural = _('Event Categories')


class EventStatus(Status):
    """
    Inherited model to contain information about an event status.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    
    """
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Status')
        verbose_name_plural = _('Event Status')


class EventStatusGroup(StatusGroup):
    """
    Inherited model to contain information about a person status group.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    :status (optional): Status in group linked by Status model
    
    """

    # Linked Fields
    status = models.ManyToManyField(EventStatus, blank=True, verbose_name="Event Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Event Status Group')
        verbose_name_plural = _('Event Status Groups')


## Main Models
class Event(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an event.

    :title (optional): 
    :slug (optional): 
    :image_upload (optional): 
    :deadline (optional): 
    :brief (optional): 
    :assigned_to (optional): 
    :manager (optional): 
    :assigned_by (optional): 
    :type (optional): 
    :status (optional): 
    :classification (optional): 
    :priority (optional): 
    :category (optional): 
    :authorisation (optional): 
    :description (optional): Description
    :private (optional): Is it private Boolean
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 

    """

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
