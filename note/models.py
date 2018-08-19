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
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Note Authorisation')
        verbose_name_plural = _('Note Authorisations')

    #def get_absolute_url(self):
    #    return reverse('Note_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    

class NoteClassification(Classification):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Note Classification')
        verbose_name_plural = _('Note Classifications')

    #def get_absolute_url(self):
    #    return reverse('Note_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class NoteType(Type):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Note Type')
        verbose_name_plural = _('Note Types')

    #def get_absolute_url(self):
    #    return reverse('Note_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class NotePriority(Priority):
    # General Fields
   
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Note Priority')
        verbose_name_plural = _('Note Priorities')

    #def get_absolute_url(self):
    #    return reverse('Note_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class NoteCategory(Category):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Note Category')
        verbose_name_plural = _('Note Categories')

    #def get_absolute_url(self):
    #    return reverse('note_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class NoteStatus(Status):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Note Status')
        verbose_name_plural = _('Note Status')

    #def get_absolute_url(self):
    #    return reverse('Note_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class NoteStatusGroup(StatusGroup):
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
    status = models.ManyToManyField(NoteStatus, blank=True, verbose_name="Note Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Note Status Group')
        verbose_name_plural = _('Note Status Groups')

    #def get_absolute_url(self):
    #    return reverse('Note_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


## Main Models
class Note(ObjectDescriptionMixin):
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


## Data Models