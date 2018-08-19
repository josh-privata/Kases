## Loan Models ##

# python imports
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from simple_history.models import HistoricalRecords
from model_utils.managers import InheritanceManager
from utils.models import ObjectDescriptionMixin, Authorisation, Category
from utils.models import Classification, Priority, Type, Status, StatusGroup
#import loan.managers as managers
from case.models import Case
from inventory.models import Device


class Request(ObjectDescriptionMixin):
    
    # These constants define choices for a device's condition
    PENDING = 'PE'
    APPROVED = 'AP'
    REJECTED = 'RE'
    HOLD = 'HO'
    WITHDRAWN = 'WI'

    # Define possible choices for condition field
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (HOLD, 'On Hold'),
        (WITHDRAWN, 'Withdrawn'),
    )
    
    # General Fields
    reason = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Reason')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING, verbose_name="Status")

    # Linked Fields   
    # Auto Fields

    history = HistoricalRecords()
    
    class Meta:
        abstract = True


class Loan(ObjectDescriptionMixin):
    
    # These constants define choices for a device's condition
    NEW = 'NW'
    EXCELLENT = 'EX'
    GOOD = 'GD'
    AVERAGE = 'AV'
    BELOW_AVERAGE = 'BA'
    POOR = 'PR'
    DAMAGED = 'DM'
    LOST = 'LO'

    # Define possible choices for condition field
    CONDITION_CHOICES = (
        (NEW, 'New'),
        (EXCELLENT, 'Excellent'),
        (GOOD, 'Good'),
        (AVERAGE, 'Average'),
        (BELOW_AVERAGE, 'Below Average'),
        (POOR, 'Poor'),
        (DAMAGED, 'Damaged'),
        (LOST, 'Lost'),
    )

    # General Fields
    reason = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Reason')
    booked_from = models.TextField(max_length=100, null=False, blank=False, verbose_name='Booked From')
    booked_until = models.TextField(max_length=100, null=False, blank=False, verbose_name='Booked Until')
    condition = models.CharField(max_length=2, choices=CONDITION_CHOICES, default=EXCELLENT, verbose_name="Device Condition")
    returned = models.BooleanField(default=False, verbose_name="Returned")

    # Linked Fields
    case = case = models.ForeignKey(Case, on_delete=models.DO_NOTHING, related_name='loan_case', blank=True, verbose_name="Case")
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING, related_name='loan_device', blank=True, verbose_name="Device")
    loaned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loaned_to', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Loaned To")
    loaned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loaned_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Loaned By")
    
    # Auto Fields

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Device Loan')
        verbose_name_plural = _('Device Loans')

    def save(self,force_insert=False, force_update=False):
        models.Model.save(self,force_insert,force_update)


class LoanRequest(Request):

    # General Fields
    booked_from = models.TextField(max_length=100, null=False, blank=False, verbose_name='Booked From')
    booked_until = models.TextField(max_length=100, null=False, blank=False, verbose_name='Booked Until')

    # Linked Fields
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING, related_name='loan_request_device', blank=True, verbose_name="Device")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loan_requested_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Requested By")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loan_approved_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Approved By")
    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING, related_name='loan_request_case', blank=True, verbose_name="Case")

    # Auto Fields
    
    class Meta:
        verbose_name = _('Loan Request')
        verbose_name_plural = _('Loan Requests')

    def save(self,force_insert=False, force_update=False):
        device = self.device

        # Change device status based on request status
        if self.status == 'PE':
            device.status = 'AW'

        if self.status == 'HO':
            device.status = 'AW' 

        if self.status == 'AP':
            device.status = 'CO'
            loan = Loan(reason=self.reason,
                        description=self.description,
                        private=self.private,
                        booked_from=self.booked_from,
                        booked_until=self.booked_until,
                        case_id=self.case_id,
                        condition=device.condition,
                        device=device,
                        returned=False,
                        loaned_to=self.requested_by,
                        loaned_by=self.rapproved_by
                        )
            loan.save()

        if self.status == 'RE':
            pass

        if self.status == 'WI':
            pass

        device.save()
        models.Model.save(self,force_insert,force_update)


class ReturnRequest(Request):

    # General Fields
    actual_use = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Actual Use Time')

    # Linked Fields
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING, related_name='return_request_device', blank=True, verbose_name="Device")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='return_requested_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Requested By")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='return_approved_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Approved By")
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING, related_name='device_loan', blank=True, verbose_name="Loan")
    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING, related_name='return_request_case', blank=True, verbose_name="Case")

    # Auto Fields
    
    class Meta:
        verbose_name = _('Return Request')
        verbose_name_plural = _('Return Requests')

    def save(self,force_insert=False, force_update=False):
        device = self.device

        # Change device status based on request status
        if self.status == 'PE':
            device.status = 'RT'

        if self.status == 'HO':
            device.status = 'RT' 

        if self.status == 'AP':
            device.status = 'NR'
            loan = self.loan
            loan.returned = True
            loan.save()

        if self.status == 'RE':
            pass

        if self.status == 'WI':
            pass

        device.save()
        models.Model.save(self,force_insert,force_update)