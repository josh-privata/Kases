## Loan Models ##

# python imports
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from simple_history.models import HistoricalRecords
from utils.models import ObjectDescriptionMixin
#import loan.managers as managers
from case.models import Case, CaseInventory
from inventory.models import Device

# Define choices for status
LOAN_PENDING = 'LP'
LOAN_APPROVED = 'LA'
LOAN_REJECTED = 'LR'
LOAN_HOLD = 'LH'
LOAN_WITHDRAWN = 'LW'
RETURN_PENDING = 'RP'
RETURN_APPROVED = 'RA'
RETURN_REJECTED = 'RR'
RETURN_HOLD = 'RH'
RETURN_WITHDRAWN = 'RW'
LOAN_CLOSED = 'CL'

STATUS_CHOICES = (
    (LOAN_PENDING, 'Loan Pending'),
    (LOAN_APPROVED, 'Loan Approved'),
    (LOAN_REJECTED, 'Loan Rejected'),
    (LOAN_HOLD, 'Loan On Hold'),
    (LOAN_WITHDRAWN, 'Loan Withdrawn'),
    (RETURN_PENDING, 'Return Pending'),
    (RETURN_APPROVED, 'Return Approved'),
    (RETURN_REJECTED, 'Return Rejected'),
    (RETURN_HOLD, 'Return On Hold'),
    (RETURN_WITHDRAWN, 'Return Withdrawn'),
    (LOAN_CLOSED, 'Loan Closed'),
)

# Define choices for condition
NEW = 'NW'
EXCELLENT = 'EX'
GOOD = 'GD'
AVERAGE = 'AV'
BELOW_AVERAGE = 'BA'
POOR = 'PR'
DAMAGED = 'DM'
LOST = 'LO'

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


class Loan(ObjectDescriptionMixin):
    """
    Model to contain information about a loan.

    :reason (optional):
    :booked_from (optional):
    :booked_until (optional):
    :condition (optional):
    :returned (optional):
    :status:
    :case (optional):
    :device (optional):
    :loaned_to (optional):
    :loaned_by (optional):
    :description (optional): Description
    :private (optional): Is it private Boolean
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 

    """

    # General Fields
    reason = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Loan Reason')
    approver_note = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Approver Note')
    booked_from = models.TextField(max_length=100, null=False, blank=False, verbose_name='Booked From')
    booked_until = models.TextField(max_length=100, null=False, blank=False, verbose_name='Booked Until')
    original_condition = models.CharField(max_length=2, choices=CONDITION_CHOICES, default=EXCELLENT, verbose_name="Original Condition")
    return_condition = models.CharField(max_length=2, choices=CONDITION_CHOICES, default=EXCELLENT, verbose_name="Returned Condition")
    returned = models.BooleanField(default=False, verbose_name="Returned")
    taken = models.BooleanField(default=False, verbose_name="Taken")
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=LOAN_PENDING, verbose_name="Status")

    # Linked Fields
    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING, related_name='loan_case', blank=True, verbose_name="Case")
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING, related_name='loan_device', blank=True, verbose_name="Device")
    loaned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loaned_to', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Loaned To")
    loaned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loaned_by', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Loaned By")
    
    # Auto Fields

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Device Loan')
        verbose_name_plural = _('Device Loans')

    def get_absolute_url(self):
        return reverse('loan_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s - %s' % (self.case, self.device)

    def save(self,force_insert=False, force_update=False):
        
        device = self.device

        # Needed as we are overriding abstract save() method
        if not self.pk:
           if device.status != 'RE':
                self.status = 'LR'
                self.approver_note = 'Device Currently On Loan'
                self.created = timezone_now()
        else:
            if not self.created:
                self.created = timezone_now()
            self.modified = timezone_now()
        
        # LOAN_PENDING = 'LP'
        if self.status == 'LP':
            device.status = 'AW'
            self.returned = True

        # LOAN_APPROVED = 'LA'
        if self.status == 'LA':
            try:
                caseinventory = CaseInventory.objects.get(case = self.case, device = self.device)
                caseinventory.reason = self.reason
                caseinventory.returned = self.returned
                caseinventory.description = self.description
                caseinventory.private = self.private
                caseinventory.status = self.status
                caseinventory.case_id = self.case_id
                caseinventory.device_id = self.device_id
                caseinventory.linked_by_id = self.loaned_by_id
                caseinventory.modified = timezone_now()
            except CaseInventory.DoesNotExist:
                caseinventory = CaseInventory(reason = self.reason,
                description = self.description,
                returned = self.returned,
                private = self.private,
                status = self.status,
                case = self.case,
                device = self.device,
                linked_by = self.loaned_by,
                created = timezone_now(),
                modified = timezone_now())
            caseinventory.save()
            device.status = 'CO'
            self.returned = True   

        # LOAN_REJECTED = 'LR'
        if self.status == 'LR':

            self.returned = True

        # LOAN_HOLD = 'LH'
        if self.status == 'LH':

            self.returned = True

        # LOAN_WITHDRAWN = 'LW'
        if self.status == 'LW':

            self.returned = True    

        # RETURN_PENDING = 'RP'
        if self.status == 'RP':

            self.returned = True    

        # RETURN_APPROVED = 'RA'
        if self.status == 'RA':

            self.returned = True   
            
        # RETURN_REJECTED = 'RR'
        if self.status == 'RP':

            self.returned = True   
            
        # RETURN_HOLD = 'RH'
        if self.status == 'RH':

            self.returned = True 
            
        # RETURN_WITHDRAWN = 'RW'
        if self.status == 'RW':

            self.returned = True    

        # LOAN_CLOSED = 'CL'
        if self.status == 'CL':

            self.returned = True    

        if not self.pk:
           self.created = timezone_now()
           #self.created_by = request.user
        else:
            if not self.created:
                self.created = timezone_now()
            self.modified = timezone_now()
        
        device.save()
        models.Model.save(self,force_insert,force_update)
