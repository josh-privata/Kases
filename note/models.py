## Note Models ##

## python imports
from django.db import models
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#import note.managers as managers
from simple_history.models import HistoricalRecords


## Admin Models
class NoteAuthorisation(Authorisation):
    """
    Inherited model to contain information about a note authorisation.

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
        verbose_name = _('Note Authorisation')
        verbose_name_plural = _('Note Authorisations')
    

class NoteClassification(Classification):
    """
    Inherited model to contain information about a note classification.

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
        verbose_name = _('Note Classification')
        verbose_name_plural = _('Note Classifications')


class NoteType(Type):
    """
    Inherited model to contain information about a note type.

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
        verbose_name = _('Note Type')
        verbose_name_plural = _('Note Types')


class NotePriority(Priority):
    """
    Inherited model to contain information about a note priority.

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
        verbose_name = _('Note Priority')
        verbose_name_plural = _('Note Priorities')


class NoteCategory(Category):
    """
    Inherited model to contain information about a note category.

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
        verbose_name = _('Note Category')
        verbose_name_plural = _('Note Categories')


class NoteStatus(Status):
    """
    Inherited model to contain information about a note status.

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
        verbose_name = _('Note Status')
        verbose_name_plural = _('Note Status')


class NoteStatusGroup(StatusGroup):
    """
    Inherited model to contain information about a note status group.

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
    status = models.ManyToManyField(NoteStatus, blank=True, verbose_name="Note Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Note Status Group')
        verbose_name_plural = _('Note Status Groups')


## Main Models
class Note(ObjectDescriptionMixin):
    """
    Abstract model to contain information about a note.

    :title (optional): 
    :slug (optional): 
    :image_upload (optional): 
    :deadline (optional): 
    :brief (optional): 
    :manager (optional): 
    :assigned_to (optional): 
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
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Note Title")
    slug = models.SlugField(blank=True, null=True, unique=True, verbose_name="Note Slug")
    image_upload = models.FileField(blank=True, null=True, verbose_name="Note Image")
    #deadline = models.DateTimeField(auto_now=False, null=True, verbose_name="Deadline")
    brief = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Brief")

    # Linked Fields
    type = models.ForeignKey(NoteType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Note Type")
    status = models.ForeignKey(NoteStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Note Status")
    classification = models.ForeignKey(NoteClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Note Classification")
    priority = models.ForeignKey(NotePriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Note Priority")
    category = models.ForeignKey(NoteCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Note Category")
    authorisation = models.ForeignKey(NoteAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Note Authorisation")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='note_assigned_to', blank=True, verbose_name="Assigned To")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='note_manager', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Note Manager")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='note_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")
    
    # Auto Fields

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.title
