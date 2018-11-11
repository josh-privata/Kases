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
    """
    Inherited model to contain information about a case authorisation.

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
        verbose_name = _('Case Authorisation')
        verbose_name_plural = _('Case Authorisations')
    

class CaseClassification(Classification):
    """
    Inherited model to contain information about a case classification.

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
        verbose_name = _('Case Classification')
        verbose_name_plural = _('Case Classifications')


class CaseType(Type):
    """
    Inherited model to contain information about a case type.

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
        verbose_name = _('Case Type')
        verbose_name_plural = _('Case Types')


class CasePriority(Priority):
    """
    Inherited model to contain information about a case priority.

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
        verbose_name = _('Case Priority')
        verbose_name_plural = _('Case Priorities')


class CaseCategory(Category):
    """
    Inherited model to contain information about a case category.

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
        verbose_name = _('Case Category')
        verbose_name_plural = _('Case Categories')


class CaseStatus(Status):
    """
    Inherited model to contain information about a case status.

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
        verbose_name = _('Case Status')
        verbose_name_plural = _('Case Status')


class CaseStatusGroup(StatusGroup):
    """
    Inherited model to contain information about a case status group.

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
    status = models.ManyToManyField(CaseStatus, blank=True, verbose_name="Case Status")

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Case Status Group')
        verbose_name_plural = _('Case Status Groups')


## Main Models
class Case(ObjectDescriptionMixin):
    """
    Model to contain information about a case.


    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model

    :id (optional): 
    :reference (optional):
    :background (optional):
    :purpose (optional):
    :location (optional):
    :brief (optional):
    :slug (optional):
    :image_upload (optional):
    :deadline (optional):
    :type (optional):
    :status (optional):
    :classification (optional):
    :priority (optional):
    :category (optional):
    :authorisation (optional):
    :assigned_to (optional):
    :managed_by (optional):
    :legal (optional):
    :client (optional):
    :assigned_by (optional):

    """

    # General Fields
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Title")
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
    """
    Model to contain information about a case link.

    :reason (optional):
    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :date_time (optional):
    :linked_by (optional):
    :case (optional):
    
    """

    # General Fields
    reason = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Reason For Link")
    date_time = models.DateTimeField(auto_now=True, null=True, verbose_name="Date")
    
    # Linked Fields
    linked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_linked_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Linked By")
    case = models.ManyToManyField(Case, blank=True, related_name='case_linked_case', verbose_name="Case")

    history = HistoricalRecords()


class CaseNote(Note):
    """
    Model to contain information about a case note.

    :title (optional):
    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :case (optional):
    
    """

    # General Fields
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")
    # Auto Fields

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
    """
    Model to contain information about case evidence.

    :title (optional):
    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :case (optional):
    
    """

    # General Fields
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")
    # Auto Fields

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
    """
    Abstract model to contain information about a case entity.

    :role (optional):
    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :notes (optional):
    :type (optional):

    """

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
    # Auto Fields

    class Meta:
        abstract = True

    @property
    def case_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('case_detail', args=(self.case.pk,))


class CasePerson(CaseEntity):
    """
    Model to contain information about a case person.

    :role (optional):
    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :notes (optional):
    :type (optional):
    :person (optional):
    :case (optional):
    :linked_by (optional):

    """

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
    # Auto Fields

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
    """
    Model to contain information about a case company.

    :role (optional):
    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :notes (optional):
    :type (optional):
    :company (optional):
    :case (optional):
    :linked_by (optional):

    """

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
    # Auto Fields

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
    """
    Model to contain information about a case inventory item.

    :reason (optional):
    :returned:
    :status:
    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :expected_use (optional):
    :device (optional):
    :case (optional):
    :linked_by (optional):

    """

    # Define choices for status
    PENDING = 'PE'
    APPROVED = 'AP'
    REJECTED = 'RE'
    HOLD = 'HO'
    WITHDRAWN = 'WI'
    TAKEN = 'TK'
    RETURNED = 'RT'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (HOLD, 'On Hold'),
        (WITHDRAWN, 'Withdrawn'),
        (TAKEN, 'Taken'),
        (RETURNED, 'Returned'),
    )

    # General Fields
    reason = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Reason')
    returned = models.BooleanField(default=False, verbose_name="Returned")
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING, verbose_name="Status")

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
    """
    Model to contain information about a case event.

    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :company (optional):
    :person (optional):
    :evidence (optional):
    :case (optional):

    """

    # General Fields
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")
    person = models.ManyToManyField(CasePerson, related_name='event_linked_person', blank=True, verbose_name="People Involved")
    company = models.ManyToManyField(CaseCompany,related_name='event_linked_company', blank=True, verbose_name="Companies Involved")
    evidence = models.ManyToManyField(CaseEvidence,related_name='event_linked_evidence', blank=True, verbose_name="Evidence Involved")
    # Auto Fields
    
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


class CaseTask(Task):
    """
    Linked model to contain information about a case task.

    :description (optional):
    :created (optional):
    :modified (optional):
    :private (optional):
    :created_by (optional):
    :modified_by (optional):
    :case (optional):
    :note (optional):
    :person (optional):
    :event (optional):
    :company (optional):
    :inventory (optional):
    :evidence (optional):

    """

    # General Fields
    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Case")
    note = models.ManyToManyField(CaseNote, related_name='task_linked_note', blank=True, verbose_name="Notes")
    event = models.ManyToManyField(CaseEvent, related_name='task_linked_event', blank=True, verbose_name="Events")
    person = models.ManyToManyField(CasePerson, related_name='task_linked_person', blank=True, verbose_name="People Involved")
    company = models.ManyToManyField(CaseCompany,related_name='task_linked_company', blank=True, verbose_name="Companies Involved")
    inventory = models.ManyToManyField(CaseInventory,related_name='task_linked_inventory', blank=True, verbose_name="Inventory Involved")
    evidence = models.ManyToManyField(CaseEvidence,related_name='task_linked_evidence', blank=True, verbose_name="Evidence Involved")
    # Auto Fields

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