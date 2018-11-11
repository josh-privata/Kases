## Evidence Models ##

## python imports
from django.db import models
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#import evidence.managers as managers
from simple_history.models import HistoricalRecords


## Admin Models
class EvidenceAuthorisation(Authorisation):
    """
    Inherited model to contain information about an evidence authorisation.

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
        verbose_name = _('Evidence Authorisation')
        verbose_name_plural = _('Evidence Authorisations')
    

class EvidenceClassification(Classification):
    """
    Inherited model to contain information about evidence classification.

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
        verbose_name = _('Evidence Classification')
        verbose_name_plural = _('Evidence Classifications')


class EvidenceType(Type):
    """
    Inherited model to contain information about evidence type.

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
        verbose_name = _('Evidence Type')
        verbose_name_plural = _('Evidence Types')


class EvidenceCategory(Category):
    """
    Inherited model to contain information about evidence category.

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
        verbose_name = _('Evidence Category')
        verbose_name_plural = _('Evidence Categories')


class EvidencePriority(Priority):
    """
    Inherited model to contain information about evidence priority.

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
        verbose_name = _('Evidence Priority')
        verbose_name_plural = _('Evidence Priorities')


class EvidenceStatus(Status):
    """
    Inherited model to contain information about evidence status.

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
        verbose_name = _('Evidence Status')
        verbose_name_plural = _('Evidence Status')


class EvidenceStatusGroup(StatusGroup):
    """
    Inherited model to contain information about evidence status group.

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
    status = models.ManyToManyField(EvidenceStatus, blank=True, verbose_name="Evidence Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Evidence Status Group')
        verbose_name_plural = _('Evidence Status Groups')


class ChainOfCustody(ObjectDescriptionMixin):
    """
    Model to contain information about evidence chain of custody.

    :date_recorded (optional):
    :date_of_custody (optional):
    :check_in (optional):
    :comment (optional):
    :custody_receipt (optional):
    :custody_receipt_label (optional):
    :assigned_to (optional):
    :assigned_by (optional):
    :custodian (optional):
    :private (optional): Is it private Boolean
    :description (optional): Description
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    
    """

    # General Fields
    date_recorded = models.DateTimeField(auto_now=True, null=True, verbose_name="Date Recorded")
    date_of_custody = models.DateTimeField(auto_now=True, null=True, verbose_name="Date of Custody")
    check_in = models.BooleanField(default=False, blank=True, verbose_name="Checked-In")
    comment = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Comment")
    custody_receipt = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Custody Receipt Number")
    custody_receipt_label = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Custody Receipt Label")
    # Linked Fields
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chainofcustody_assigned_to', blank=True, verbose_name="Assigned To")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chainofcustody_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")
    custodian = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chainofcustody_custodian', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Custodian")
    
    history = HistoricalRecords()


## Main Models
class Evidence(ObjectDescriptionMixin):
    """
    Abstract model to contain information about evidence.

    :title (optional): 
    :reference (optional): 
    :comment (optional): 
    :bag_number (optional): 
    :location (optional): 
    :uri (optional): 
    :current_status (optional): 
    :qr_code_text (optional): 
    :qr_code (optional): 
    :retention_reminder_sent (optional): 
    :retention_start_date (optional): 
    :retention_date (optional): 
    :deadline (optional): 
    :brief (optional): 
    :chain_of_custody (optional): 
    :custodian (optional): 
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
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Evidence Title")
    reference = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Evidence Reference")
    comment = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Comment")
    bag_number = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Bag Number")
    location = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Physical Location")
    uri = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="File Location")
    current_status = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Current Status")
    qr_code_text = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="QR Code Text")
    qr_code = models.BooleanField(default=False, blank=True, verbose_name="QR Code")
    retention_reminder_sent = models.BooleanField(default=False, blank=True, verbose_name="Retention Reminder")
    slug = models.SlugField(blank=True, null=True, unique=True, verbose_name="Evidence Slug")
    #deadline = models.DateTimeField(auto_now=False, null=True, verbose_name="Deadline")
    retention_date = models.DateTimeField(auto_now=False, blank=True, null=True, verbose_name="Retention Date")
    brief = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Case Brief")

    # Linked Fields
    chain_of_custody = models.ForeignKey(ChainOfCustody, on_delete=models.SET_NULL, related_name='evidence_chain_of_custody', blank=True, null=True, verbose_name="Chain Of Custody")
    custodian = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='evidence_custodian', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Custodian")
    type = models.ForeignKey(EvidenceType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Type")
    status = models.ForeignKey(EvidenceStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Status")
    classification = models.ForeignKey(EvidenceClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Classification")
    priority = models.ForeignKey(EvidencePriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Priority")
    authorisation = models.ForeignKey(EvidenceAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Authorisation")
    category = models.ForeignKey(EvidenceCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Category")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='evidence_assigned_to', blank=True, verbose_name="Assigned To")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='evidence_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")

    # Auto Fields
    retention_start_date = models.DateTimeField(auto_now=True, null=True, verbose_name="Retention Start Date")
    
    # Data Models

    history = HistoricalRecords()

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
