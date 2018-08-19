## Case Models ##

## python imports
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from utils.models import ObjectDescriptionMixin, Authorisation, Category
from utils.models import Classification, Priority, Type, Status, StatusGroup
#import case.managers as managers
from note.models import Note
from event.models import Event
from task.models import Task
from evidence.models import Evidence
from entity.models.person import Person
from entity.models.company import Company
from inventory.models import Device


## Admin Models
class CaseAuthorisation(Authorisation):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Case Authorisation')
        verbose_name_plural = _('Case Authorisations')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    

class CaseClassification(Classification):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Case Classification')
        verbose_name_plural = _('Case Classifications')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CaseType(Type):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Case Type')
        verbose_name_plural = _('Case Types')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CasePriority(Priority):
    # General Fields
   
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Case Priority')
        verbose_name_plural = _('Case Priorities')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CaseCategory(Category):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Case Category')
        verbose_name_plural = _('Case Categories')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CaseStatus(Status):
    # General Fields
    
    history = HistoricalRecords()

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
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Case Status Group')
        verbose_name_plural = _('Case Status Groups')

    #def get_absolute_url(self):
    #    return reverse('case_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


## Main Models
class Case(ObjectDescriptionMixin):
    """
    Model to contain information about a booking.

    Note, that on the model itself, most of the attributes are blank=True.
    We need this behaviour to be able to create empty temporary bookings.
    You will have to take care of the field being required or not in a
    ModelForm yourself.

    :user (optional): Connection to Django's User model.
    :session (optional): Stored session to identify anonymous users.
    :gender (optional): Gender of the user.
    :title (optional): Title of the user.
    :forename (optional): First name of the user.
    :surname (optional): Last name of the user.
    :nationality (optional): The nationality of the user.
    :street1 (optional): Street address of the user.
    :street2 (optional): Additional street address of the user.
    :city (optional): City of the user's address.
    :zip_code (optional): ZIP of the user's address.
    :country (optional): Country of the user's address.
    :phone (optional): Phone number of the user.
    :email: Email of the user.
    :special_request (optional): A special request of the customer.
    :date_from (optional): From when the booking is active.
    :date_until (optional): Until when the booking is active.
    :time_period (optional): How long the period from date_from will be eg. 10 (days).
    :time_unit (optional): What unit of time the period is of. e.g. nights or days.
    :creation_date: Date of the booking.
    :booking_id (optional): Custom unique booking identifier.
    :booking_status: Current status of the booking.
    :notes (optional): Staff notes.
    :total (optional): Field for storing a total of all items.
    :currency (optional): If total is uses, we usually also need a currency.

    """

    # General Fields
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Title")
    #description= models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Description")
    reference = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Reference")
    background = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Background")
    purpose = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Purpose")
    location = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Location")
    brief = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Brief")
    slug = models.SlugField(blank=True, null=True, unique=True, verbose_name="Case Slug")
    image_upload = models.FileField(blank=True, null=True, verbose_name="Case Image")
    #deadline = models.DateTimeField(auto_now=False, null=True, verbose_name="Deadline")

    # Linked Fields
    type = models.ForeignKey(CaseType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Type")
    status = models.ForeignKey(CaseStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Status")
    classification = models.ForeignKey(CaseClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Classification")
    priority = models.ForeignKey(CasePriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Priority")
    category = models.ForeignKey(CaseCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Category")
    authorisation = models.ForeignKey(CaseAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case Authorisation")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='case_assigned_to', blank=True, verbose_name="Assigned To")
    managed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_manager', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Case Manager")
    #legal = models.ManyToManyField(Personality, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Legal Advisor")
    #client = models.ManyToManyField(Personality, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Client")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")
    
    # Auto Fields
    
    history = HistoricalRecords()

    #manager = CaseManager()

    class Meta:
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


## Linked Models
class LinkedCase(ObjectDescriptionMixin):
    # General Fields
    reason = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Reason For Link")
    date_time = models.DateTimeField(auto_now=True, null=True, verbose_name="Date")
    
    # Linked Fields
    linked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_linked_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Linked By")
    case = models.ManyToManyField(Case, blank=True, related_name='case_linked_case', verbose_name="Case")


class CaseNote(Note):
    # General Fields
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Case Note')
        verbose_name_plural = _('Case Notes')
        #abstract = True

    @property
    def edit_url(self):
        """Returns the url for the edit page for this case."""
        return reverse('casenote_edit', args=(self.case.pk, self.pk))

    @property
    def case_url(self):
        '''Returns the url for the detail page of this case'''
        return reverse('case_detail', args=(self.case.pk,))

    def get_absolute_url(self):
        '''Returns the absolute url'''
        return reverse('casenote_detail', kwargs={'pk': self.pk})


class CaseEvidence(Evidence):
    # General Fields
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Case Evidence')
        verbose_name_plural = _('Case Evidence')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('caseevidence_edit', args=(self.case.pk, self.pk))

    @property
    def case_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('case_detail', args=(self.case.pk,))

    def get_absolute_url(self):
        '''Returns the absolute url'''
        return reverse('caseevidence_detail', kwargs={'pk': self.pk})


class CaseEntity(ObjectDescriptionMixin):

    # These constants define choices for a device's status
    RELATED = 'RL'
    UNRELATED = 'UR'
    UNKNOWN = 'UN'
    SUSPECT = 'SU'
    ASSISTING = 'AS'
    INFORMANT = 'IN'
    ACQUAINTANCE = 'AQ'
    VICTIM = 'VI'
    WORKING = 'WK'


    # Define possible choices for condition field
    TYPE_CHOICES = (
        (RELATED, 'Related'),
        (UNRELATED, 'Unrelated'),
        (UNKNOWN, 'Unknown'),
        (SUSPECT, 'Suspect'),
        (INFORMANT, 'Informant'),
        (ACQUAINTANCE, 'Acquaintance'),
        (VICTIM, 'Victim'),
        (WORKING, 'Working'),
        (ASSISTING, 'Assisting'),
    )

    # General Fields
    role = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Role")
    notes = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Notes")
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=UNKNOWN, verbose_name="Type")

    # Linked Fields
   

    class Meta:
        abstract = True

    @property
    def case_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('case_detail', args=(self.case.pk,))


class CasePerson(CaseEntity):
    # These constants define choices for a device's status
    RELATED = 'RL'
    UNRELATED = 'UR'
    UNKNOWN = 'UN'
    SUSPECT = 'SU'
    ASSISTING = 'AS'
    INFORMANT = 'IN'
    ACQUAINTANCE = 'AQ'
    VICTIM = 'VI'
    WORKING = 'WK'


    # Define possible choices for condition field
    TYPE_CHOICES = (
        (RELATED, 'Related'),
        (UNRELATED, 'Unrelated'),
        (UNKNOWN, 'Unknown'),
        (SUSPECT, 'Suspect'),
        (INFORMANT, 'Informant'),
        (ACQUAINTANCE, 'Acquaintance'),
        (VICTIM, 'Victim'),
        (WORKING, 'Working'),
        (ASSISTING, 'Assisting'),
    )

    # General Fields

    # Linked Fields
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, verbose_name="Person")
    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING, related_name='person_linked_case', blank=True, verbose_name="Case")
    linked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='person_linked_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Linked By")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Case Person')
        verbose_name_plural = _('Case Persons')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('caseperson_edit', args=(self.case.pk, self.pk))

    def get_absolute_url(self):
        '''Returns the absolute url'''
        return reverse('caseperson_detail', kwargs={'pk': self.pk})


class CaseCompany(CaseEntity):
     # These constants define choices for a device's status
    RELATED = 'RL'
    UNRELATED = 'UR'
    UNKNOWN = 'UN'
    SUSPECT = 'SU'
    ASSISTING = 'AS'
    INFORMANT = 'IN'
    ACQUAINTANCE = 'AQ'
    VICTIM = 'VI'
    WORKING = 'WK'


    # Define possible choices for condition field
    TYPE_CHOICES = (
        (RELATED, 'Related'),
        (UNRELATED, 'Unrelated'),
        (UNKNOWN, 'Unknown'),
        (SUSPECT, 'Suspect'),
        (INFORMANT, 'Informant'),
        (ACQUAINTANCE, 'Acquaintance'),
        (VICTIM, 'Victim'),
        (WORKING, 'Working'),
        (ASSISTING, 'Assisting'),
    )

    # General Fields

    # Linked Fields
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, verbose_name="Company")
    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING, related_name='company_linked_case', blank=True, verbose_name="Case")
    linked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='company_linked_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Linked By")

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Case Company')
        verbose_name_plural = _('Case Companies')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('casecompany_edit', args=(self.case.pk, self.pk))

    def get_absolute_url(self):
        '''Returns the absolute url'''
        return reverse('casecompany_detail', kwargs={'pk': self.pk})


class CaseInventory(ObjectDescriptionMixin):
    # General Fields
    reason = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Reason')
    expected_use = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Expected Use Time')

    # Linked Fields
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING, related_name='device', blank=True, verbose_name="Device")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case', blank=True, null=True, verbose_name="Case")
    linked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='casedevice_linked_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Linked By")
    
    # Auto Fields

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Case Device')
        verbose_name_plural = _('Case Devices')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('casedevice_edit', args=(self.case.pk, self.pk))

    @property
    def case_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('case_detail', args=(self.case.pk,))

    def get_absolute_url(self):
        '''Returns the absolute url'''
        return reverse('casedevice_detail', kwargs={'pk': self.pk})

    def save(self,force_insert=False, force_update=False):
        models.Model.save(self,force_insert,force_update)


class CaseEvent(Event):
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")
    person = models.ManyToManyField(Person, related_name='event_linked_person', through='EventPerson', blank=True, verbose_name="People Involved")
    company = models.ManyToManyField(Company,related_name='event_linked_company', through='EventCompany', blank=True, verbose_name="Companies Involved")
    evidence = models.ManyToManyField(CaseEvidence,related_name='event_linked_evidence', blank=True, verbose_name="Evidence Involved")

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Case Event')
        verbose_name_plural = _('Case Event')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('caseevent_edit', args=(self.case.pk, self.pk))

    @property
    def case_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('case_detail', args=(self.case.pk,))

    def get_absolute_url(self):
        '''Returns the absolute url'''
        return reverse('caseevent_detail', kwargs={'pk': self.pk})


class EventPerson(CaseEntity):
    # General Fields
    # Linked Fields
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(CaseEvent, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Event Person')
        verbose_name_plural = _('Event Persons')


class EventCompany(CaseEntity):
    # General Fields
    # Linked Fields
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    event = models.ForeignKey(CaseEvent, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Event Company')
        verbose_name_plural = _('Event Companies')


class CaseTask(Task):
    # General Fields
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")
    note = models.ManyToManyField(CaseNote, related_name='task_linked_note', blank=True, verbose_name="Notes")
    event = models.ManyToManyField(CaseEvent, related_name='task_linked_event', blank=True, verbose_name="Events")
    person = models.ManyToManyField(CasePerson, related_name='task_linked_person', blank=True, verbose_name="People Involved")
    company = models.ManyToManyField(CaseCompany,related_name='task_linked_company', blank=True, verbose_name="Companies Involved")
    inventory = models.ManyToManyField(CaseInventory,related_name='task_linked_inventory', blank=True, verbose_name="Inventory Involved")
    evidence = models.ManyToManyField(CaseEvidence,related_name='task_linked_evidence', blank=True, verbose_name="Evidence Involved")

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Case Task')
        verbose_name_plural = _('Case Task')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('casetask_edit', args=(self.case.pk, self.pk))

    @property
    def case_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('case_detail', args=(self.case.pk,))

    def get_absolute_url(self):
        '''Returns the absolute url'''
        return reverse('casetask_detail', kwargs={'pk': self.pk})