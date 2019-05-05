## Task Models ##

## python imports
import itertools
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from utils.models import ObjectDescription
from utils.models import Authorisation
from utils.models import BaseObject
from utils.models import Priority
from utils.models import Note
#import task.managers as managers


## Admin Models
class TaskCategory(BaseObject):
    """ Model to contain information about a task type.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        title (str) [50]: Title
        colour (str, optional) [7]: Hexidecimal colour representation
        description (str, optional) [1000]: Description
        created (date, auto): Date Created
        modified (date,auto): Date Modified
        created_by (User, auto): Created by
        modified_by (User, auto): Modified by 
    
    """

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Task Category')
        verbose_name_plural = _('Task Categories')


class TaskStatus(BaseObject):
    """ Model to contain information about a task status.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        title (str) [50]: Title
        colour (str, optional) [7]: Hexidecimal colour representation
        description (str, optional) [1000]: Description
        created (date, auto): Date Created
        modified (date,auto): Date Modified
        created_by (User, auto): Created by
        modified_by (User, auto): Modified by
    
    """
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Task Status')
        verbose_name_plural = _('Task Status')


class TaskStatusGroup(BaseObject):
    """ Model to contain information about a task status group.

    Args:
        status (TaskStatus): Status in group
        history (HistoricalRecord, auto): Historical records of object
        title (str) [50]: Title
        colour (str, optional) [7]: Hexidecimal colour representation
        description (str, optional) [1000]: Description
        created (date, auto): Date Created
        modified (date,auto): Date Modified
        created_by (User, auto): Created by
        modified_by (User, auto): Modified by
    
    """

    # Linked Fields
    status = models.ManyToManyField(
        TaskStatus, 
        blank=True, 
        verbose_name=_("Task Status"),
        help_text=_("Select Task Status"))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Task Status Group')
        verbose_name_plural = _('Task Status Groups')


## Main Models
class Task(ObjectDescription):


    ## General Fields ##
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        verbose_name=_("Title"),
        help_text=_("Enter a title for the Task"))

    location = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        default=None,
        verbose_name=_("Location"),
        help_text=_("(Optional) Enter a location for the task"))

    #deadline = models.DateTimeField(
    #   auto_now=False, 
    #   null=False,
    #   default=timezone.now(), 
    #   verbose_name=_("Deadline"),
    #   help_text=_("Select a deadline for the Task"))

    ## Linked Fields ##

    category = models.ForeignKey(
        TaskCategory, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        verbose_name=_("Category"),
        help_text=_("(Optional) Select the category of Task"))

    status = models.ForeignKey(
        TaskStatus, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        verbose_name=_("Status"),
        help_text=_("(Optional) Select the status of the Task"))

    priority = models.ForeignKey(
        Priority, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        verbose_name=_("Priority"),
        help_text=_("(Optional) Select the priority of the Task"))

    authorisation = models.ForeignKey(
        Authorisation, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        verbose_name=_("Authorisation"),
        help_text=_("(Optional) Select the authorisation of the Task"))

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='task_manager', 
        verbose_name=_("Task Manager"),
        help_text=_("(Optional) Select the Task Manager"))

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='task_assigned_by', 
        verbose_name=_("Assigned By"),
        help_text=_("(Optional) Select Task assigned by"))

    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        blank=True,
        related_name='task_assigned_to', 
        verbose_name=_("Assigned To"),
        help_text=_("(Optional) Select Task assigned to"))

    note = models.ManyToManyField(
        Note, 
        blank=True, 
        related_name='task_note', 
        verbose_name=_("Note"),
        help_text=_("(Optional) Enter a note relating to the Task"))

    ## Auto Fields ##
    slug = models.SlugField(
        blank=True, 
        null=True, 
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("A slug value representing title"))


    class Meta:
        abstract = True

    def __str__(self):
        """ Returns a human friendly string
        
        Returns:
            Title

        """
        return '%s' % _(self.title)
