## Task Models ##

## python imports
from django.db import models
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#import task.managers as managers
from simple_history.models import HistoricalRecords


## Admin Models
class TaskAuthorisation(Authorisation):
    """
    Inherited model to contain information about a task authorisation.

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
        verbose_name = _('Task Authorisation')
        verbose_name_plural = _('Task Authorisations')
    

class TaskClassification(Classification):
    """
    Inherited model to contain information about a task classification.

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
        verbose_name = _('Task Classification')
        verbose_name_plural = _('Task Classifications')


class TaskType(Type):
    """
    Inherited model to contain information about a task type.

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
        verbose_name = _('Task Type')
        verbose_name_plural = _('Task Types')


class TaskPriority(Priority):
    """
    Inherited model to contain information about a task priority.

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
        verbose_name = _('Task Priority')
        verbose_name_plural = _('Task Priorities')


class TaskCategory(Category):
    """
    Inherited model to contain information about a task category.

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
        verbose_name = _('Task Category')
        verbose_name_plural = _('Task Categories')


class TaskStatus(Status):
    """
    Inherited model to contain information about a task status.

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
        verbose_name = _('Task Status')
        verbose_name_plural = _('Task Status')


class TaskStatusGroup(StatusGroup):
    """
    Inherited model to contain information about a task status group.

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
    status = models.ManyToManyField(TaskStatus, blank=True, verbose_name="Task Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Task Status Group')
        verbose_name_plural = _('Task Status Groups')


## Main Models
class Task(ObjectDescriptionMixin):
    """
    Abstract model to contain information about a task.

    :title (optional): 
    :slug (optional): 
    :background (optional): 
    :deadline (optional): 
    :brief (optional): 
    :location (optional): 
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
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Task Title")
    background = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Task Background")
    location = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Task Location")
    #deadline = models.DateTimeField(auto_now=False, null=True, verbose_name="Deadline")
    slug = models.SlugField(blank=True, null=True, unique=True, verbose_name="Evidence Slug")
    brief = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Brief")

    # Linked Fields
    type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Type")
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Status")
    classification = models.ForeignKey(TaskClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Classification")
    priority = models.ForeignKey(TaskPriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Priority")
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Category")
    authorisation = models.ForeignKey(TaskAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Authorisation")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='task_assigned_to', blank=True, verbose_name="Assigned To")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_manager', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Task Manager")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")

    # Auto Fields

    history = HistoricalRecords()

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title