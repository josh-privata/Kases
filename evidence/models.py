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
    # General Fields

    class Meta:
        verbose_name = _('Evidence Authorisation')
        verbose_name_plural = _('Evidence Authorisations')

    #def get_absolute_url(self):
    #    return reverse('Evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    

class EvidenceClassification(Classification):
    # General Fields
    
    class Meta:
        verbose_name = _('Evidence Classification')
        verbose_name_plural = _('Evidence Classifications')

    #def get_absolute_url(self):
    #    return reverse('Evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EvidenceType(Type):
    # General Fields
    
    class Meta:
        verbose_name = _('Evidence Type')
        verbose_name_plural = _('Evidence Types')

    #def get_absolute_url(self):
    #    return reverse('Evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EvidenceCategory(Category):
    # General Fields
    
    class Meta:
        verbose_name = _('Evidence Category')
        verbose_name_plural = _('Evidence Categories')

    #def get_absolute_url(self):
    #    return reverse('Evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EvidencePriority(Priority):
    # General Fields
   
    class Meta:
        verbose_name = _('Evidence Priority')
        verbose_name_plural = _('Evidence Priorities')

    #def get_absolute_url(self):
    #    return reverse('Evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EvidenceStatus(Status):
    # General Fields

    class Meta:
        verbose_name = _('Evidence Status')
        verbose_name_plural = _('Evidence Status')

    #def get_absolute_url(self):
    #    return reverse('Evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class EvidenceStatusGroup(StatusGroup):
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
    status = models.ManyToManyField(EvidenceStatus, blank=True, verbose_name="Evidence Status")

    class Meta:
        verbose_name = _('Evidence Status Group')
        verbose_name_plural = _('Evidence Status Groups')

    #def get_absolute_url(self):
    #    return reverse('Evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class ChainOfCustody(ObjectDescriptionMixin):
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


## Main Models
class Evidence(ObjectDescriptionMixin):
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

    # Linked Fields
    type = models.ForeignKey(EvidenceType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Type")
    status = models.ForeignKey(EvidenceStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Status")
    classification = models.ForeignKey(EvidenceClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Classification")
    priority = models.ForeignKey(EvidencePriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Priority")
    authorisation = models.ForeignKey(EvidenceAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Authorisation")
    category = models.ForeignKey(EvidenceCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Evidence Category")
    chain_of_custody = models.ForeignKey(ChainOfCustody, on_delete=models.SET_NULL, related_name='evidence_chain_of_custody', blank=True, null=True, verbose_name="Chain Of Custody")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='evidence_assigned_to', blank=True, verbose_name="Assigned To")
    custodian = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='evidence_custodian', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Custodian")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='evidence_assigned_by', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned By")

    # Auto Fields
    retention_date = models.DateTimeField(auto_now=True, null=True, verbose_name="Retention Date")
    date_added = models.DateTimeField(auto_now=True, null=True, verbose_name="Date Added")
    deadline = models.DateTimeField(auto_now=True, null=True, verbose_name="Deadline")
    retention_start_date = models.DateTimeField(auto_now=True, null=True, verbose_name="Retention Start Date")
    
    # Data Models

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Evidence')
        verbose_name_plural = _('Evidence')
        #abstract = True

    def get_absolute_url(self):
        return reverse('evidence_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
