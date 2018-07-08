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
    # General Fields

    class Meta:
        verbose_name = _('Task Authorisation')
        verbose_name_plural = _('Task Authorisations')

    #def get_absolute_url(self):
    #    return reverse('Task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    

class TaskClassification(Classification):
    # General Fields
    
    class Meta:
        verbose_name = _('Task Classification')
        verbose_name_plural = _('Task Classifications')

    #def get_absolute_url(self):
    #    return reverse('Task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class TaskType(Type):
    # General Fields
    
    class Meta:
        verbose_name = _('Task Type')
        verbose_name_plural = _('Task Types')

    #def get_absolute_url(self):
    #    return reverse('Task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class TaskPriority(Priority):
    # General Fields
   
    class Meta:
        verbose_name = _('Task Priority')
        verbose_name_plural = _('Task Priorities')

    #def get_absolute_url(self):
    #    return reverse('Task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class TaskCategory(Category):
    # General Fields
    
    class Meta:
        verbose_name = _('Task Category')
        verbose_name_plural = _('Task Categories')

    #def get_absolute_url(self):
    #    return reverse('task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class TaskStatus(Status):
    # General Fields

    class Meta:
        verbose_name = _('Task Status')
        verbose_name_plural = _('Task Status')

    #def get_absolute_url(self):
    #    return reverse('Task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class TaskStatusGroup(StatusGroup):
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
    status = models.ManyToManyField(TaskStatus, blank=True, verbose_name="Task Status")

    class Meta:
        verbose_name = _('Task Status Group')
        verbose_name_plural = _('Task Status Groups')

    #def get_absolute_url(self):
    #    return reverse('Task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


## Main Models
class Task(ObjectDescriptionMixin):
    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Task Title")
    background = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Task Background")
    location = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Task Location")
    private = models.BooleanField(default=False, blank=True, verbose_name="Private")
    slug = models.SlugField(blank=True, null=True, unique=True, verbose_name="Evidence Slug")

    # Linked Fields
    type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Type")
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Status")
    classification = models.ForeignKey(TaskClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Classification")
    priority = models.ForeignKey(TaskPriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Priority")
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Category")
    authorisation = models.ForeignKey(TaskAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Task Authorisation")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='task_assigned_to', blank=True, verbose_name="Assigned To")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_manager', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Case Manager")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")

    # Auto Fields
    date_added = models.DateTimeField(auto_now=True, null=True, verbose_name="Date Added")
    deadline = models.DateTimeField(auto_now=True, null=True, verbose_name="Deadline")

    # Data Models

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        #abstract = True

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title