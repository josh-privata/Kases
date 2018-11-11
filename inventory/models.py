## Inventory Models ##

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
#import case.managers as managers
from note.models import Note
from task.models import Task
from evidence.models import Evidence
from entity.models.company import Company
from entity.models.person import Person

'''
Data Storage
Data Aquisition
Device Storage
Computer
Computer Peripheral
Networking
Software
Vehicle
Site Equipment
Audio Recorder
Audio Player
Clothing
Still Camera
Video Camera
Optics
Display
Power
Case
Book
Tracking
Phone
Counter Intelligence
Misc
Tools
Gadget
Chip Analysis
Cable
'''


# These constants define choices for a device's status
CHECKED_IN_READY = 'RE'
CHECKED_IN_NOT_READY = 'NR'
CHECKED_OUT = 'CO'
AWAITING_LOAN = 'AW'
AWAITING_RETURN = 'RT'
STORAGE = 'ST'
DAMAGED = 'DM'
REPLACE = 'RE'
MISSING = 'MI'
DECOMMISIONED = 'DE'
OBSELETE = 'OB'
RESTRICTED = 'RS'
HOLD = 'HO'
SERVICING = 'SE'

# Define possible choices for status field
STATUS_CHOICES = (
    (CHECKED_IN_READY, 'Checked In - Ready'),
    (CHECKED_IN_NOT_READY, 'Checked In - Not Ready'),
    (CHECKED_OUT, 'Checked Out'),
    (AWAITING_LOAN, 'Awaiting Loan Approval'),
    (AWAITING_RETURN, 'Awaiting Return Approval'),
    (STORAGE, 'In Storage'),
    (DAMAGED, 'Damaged'),
    (REPLACE, 'Replacement Required'),
    (MISSING, 'Missing'),
    (DECOMMISIONED, 'Decommisioned'),
    (OBSELETE, 'Obselete'),
    (RESTRICTED, 'Restricted Use'),
    (HOLD, 'On Hold'),
    (SERVICING, 'Servicing'),
)

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


## Admin Models
class DeviceAuthorisation(Authorisation):
    """
    Inherited model to contain information about a device authorisation.

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
        verbose_name = _('Device Classification')
        verbose_name_plural = _('Device Classifications')
    

class DeviceClassification(Classification):
    """
    Inherited model to contain information about a device classification.

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
        verbose_name = _('Device Classification')
        verbose_name_plural = _('Device Classifications')


class DeviceType(Type):
    """
    Inherited model to contain information about a device type.

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
        verbose_name = _('Device Type')
        verbose_name_plural = _('Device Types')


class DeviceCategory(Category):
    """
    Inherited model to contain information about a device category.

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
        verbose_name = _('Device Category')
        verbose_name_plural = _('Device Categories')


class DeviceStatus(Status):
    """
    Inherited model to contain information about a device status.

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
        verbose_name = _('Device Status')
        verbose_name_plural = _('Device Status')


class DeviceStatusGroup(StatusGroup):
    """
    Inherited model to contain information about a device status group.

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
    status = models.ManyToManyField(DeviceStatus, blank=True, verbose_name="Device Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Device Status Group')
        verbose_name_plural = _('Device Status Groups')


class ServiceContract(ObjectDescriptionMixin):
    """
    Model to contain information about a device service contract.

    :title (optional): 
    :duration (optional): 
    :contract_id (optional): 
    :service_id (optional): 
    :terms (optional): 
    :renewal_date (optional): 
    :renewal_cost (optional): 
    :vendor (optional): 
    :contact (optional): 
    :document (optional): 
    :responsible (optional): 
    :description (optional): Description
    :private (optional): Is it private Boolean
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 

    """

    # General Fields
    title = models.CharField(max_length=64, blank=True, null=True, verbose_name="Contract Title")
    duration = models.CharField(max_length=16, blank=True, null=True, verbose_name="Contract Duration")
    contract_id = models.CharField(max_length=45, blank=True, null=True, verbose_name="Service Contract ID")
    service_id = models.CharField(max_length=45, blank=True, null=True, verbose_name="Service ID")
    terms = models.CharField(max_length=64, blank=True, null=True, verbose_name="Terms and Conditions")
    renewal_date = models.CharField(max_length=64, blank=True, null=True, verbose_name="Renewal Date")
    renewal_cost = models.CharField(max_length=64, blank=True, null=True, verbose_name="Renewal Cost")

    # Linked Fields
    vendor = models.CharField(max_length=64, blank=True, null=True, verbose_name="Contract Vendor")
    contact = models.CharField(max_length=128, blank=True, null=True, verbose_name="Contract Contact")
    #document = models.CharField(max_length=64, blank=True, null=True, verbose_name="Service Contract")
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='responsible_for_contract',
                                    on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Resposnsible Party")

    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service Contract')
        verbose_name_plural = _('Service Contracts')


## Main Models

class Device(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an event.
 
    :title (optional): 
    :make (optional): 
    :model (optional): 
    :purpose (optional): 
    :variation (optional): 
    :serial_number (optional): 
    :status (optional): 
    :condition (optional): 
    :returnable (optional): 
    :service_id (optional): 
    :model_number (optional): 
    :warranty_title (optional): 
    :warranty_contact (optional): 
    :warranty_duration (optional): 
    :warranty_id (optional): 
    :warranty_terms (optional): 
    :warranty_start (optional): 
    :warranty_end (optional): 
    :warranty_extended (optional): 
    :warranty_vendor (optional): 
    :warranty_responsible (optional): 
    :purchased (optional): 
    :manufacturer (optional): 
    :rep (optional): 
    :vendor (optional): 
    :service_contract (optional): 
    :resposible_party (optional):
    :device_dependency (optional):
    :related_devices (optional):
    :warranty_document (optional):
    :instruction_document (optional):
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
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name="Device Title")
    make = models.CharField(max_length=200, null=True, blank=True, verbose_name="Device Make")
    model = models.CharField(max_length=200, null=True, blank=True, verbose_name="Device Model")
    purpose = models.CharField(max_length=200, null=True, blank=True, verbose_name="Device Purpose")
    variation = models.CharField(max_length=200, null=True, blank=True, verbose_name="Device Variation")
    serial_number = models.CharField(max_length=200, null=True, blank=True, verbose_name="Serial Number")
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=CHECKED_IN_READY, verbose_name="Device Status")
    condition = models.CharField(max_length=2, choices=CONDITION_CHOICES, default=EXCELLENT, verbose_name="Device Condition")
    returnable = models.BooleanField(default=True, verbose_name="Returnable To Stock")
    service_id = models.CharField(max_length=45, blank=True, null=True, verbose_name="Device Service ID")
    model_number = models.CharField(max_length=16, blank=True, null=True, verbose_name="Device Model Number")
    warranty_title = models.CharField(max_length=64, blank=True, null=True, verbose_name="Warranty Title")
    warranty_contact = models.CharField(max_length=128, blank=True, null=True, verbose_name="Warranty Contract")
    warranty_duration = models.CharField(max_length=16, blank=True, null=True, verbose_name="Warranty Duration")
    warranty_id = models.CharField(max_length=45, blank=True, null=True, verbose_name="Warranty ID")
    warranty_terms = models.CharField(max_length=64, blank=True, null=True, verbose_name="Warranty Terms and Conditions")
    warranty_start = models.DateTimeField('Warranty Start Date', blank=True, null=True)
    warranty_end = models.DateTimeField('Warranty End Date', blank=True, null=True)
    warranty_extended = models.BooleanField(default=False, verbose_name="Extended Warranty")
    purchased = models.DateTimeField('Purchase Date', blank=True, null=True)

    # Linked Fields
    #device_dependency = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, verbose_name="Device Dependency")
    #related_devices = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, verbose_name="Related Devices")
    manufacturer = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='manufacturer', blank=True, null=True, verbose_name="Device Manufacturer")
    rep = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sales_rep', blank=True, null=True, verbose_name="Vendor Sales Rep")
    vendor = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vendor', blank=True, null=True, verbose_name="Device Vendor")
    service_contract = models.ForeignKey(ServiceContract, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Device Service Contract")
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Device Type")
    classification = models.ForeignKey(DeviceClassification, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Device Classification")
    category = models.ForeignKey(DeviceCategory, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Device Category")
    authorisation = models.ForeignKey(DeviceAuthorisation, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Device Authorisation")
    resposible_party = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='resposible_party', on_delete=models.CASCADE,
                                         blank=True, null=True, verbose_name="Device Manager")
    warranty_vendor = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='warranty_vendor', blank=True, null=True, verbose_name="Warranty Vendor")
    #warranty_document = models.CharField(max_length=64, blank=True, null=True, verbose_name="Warranty Document")
    #instruction_document = models.CharField(max_length=64, blank=True, null=True, verbose_name="Instruction Document")
    warranty_responsible = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='responsible_for_warranty',
                                    on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Resposnsible For Warranty")

    
    # Auto Fields
    slug = models.SlugField(editable=False, null=True, blank=True, verbose_name="Device Slug")
    
    history = HistoricalRecords()  

    #class Meta:
        #abstract = True
        #permissions = (
        #    ('can_change_device_status', "Can change device status"),
        #    ('can_update_device_attributes', "Can update device attributes")
        #)
        #get_latest_by = 'created_at'

    def __str__(self):
        return '%s' % self.title
    
    def get_absolute_url(self):
        '''Returns the absolute url'''
        if not (self.slug):
            self.save(force_update=True)
        return reverse('device_detail',args=[self.pk])

    def get_status_color(self):
        '''Return a css color that corresponds to the device's status.
        '''
        if self.status in [Device.CHECKED_IN_NOT_READY,
                            Device.BROKEN]:
            return 'red'
        elif self.status in [Device.CHECKED_IN_READY, Device.CHECKED_IN]:
            return 'green'
        elif self.status in [Device.CHECKED_OUT]:
            return '#ffcc00'

    def check_in(self, condition='excellent'):
        """Checks in a device.

        Args:
        condition - String indicating the condition of
                    the device. Must either 'excellent', 'broken',
                    'missing', or 'scratched'.

        """
        if condition == 'broken':
            self.status = Device.BROKEN
            self.condition = Device.BROKEN
        elif condition == 'scratched':
            self.condition = Device.SCRATCHED
            self.status = Device.CHECKED_IN
        elif condition == 'missing':
            self.condition = Device.MISSING
            self.status = Device.MISSING
        else:
            self.condition = Device.EXCELLENT
            self.status = Device.CHECKED_IN

        return self.save()

    def check_out(self):
        '''Checks out a device.
        '''
        self.status = Device.CHECKED_OUT
        return self.save()

    def save(self,force_insert=False, force_update=False):
        from django.template.defaultfilters import slugify
        if not self.pk:
           self.created = timezone_now()
           #self.created_by = request.user
        else:
            if not self.created:
                self.created = timezone_now()
            self.modified = timezone_now()
        if not self.slug:
            self.slug = slugify(self.title)
        models.Model.save(self,force_insert,force_update)


class Service(ObjectDescriptionMixin):
    """
    Model to contain information about a device service.

    :issue (optional): 
    :resolution (optional): 
    :work_done (optional): 
    :left_inventory (optional): 
    :return_date (optional): 
    :cost (optional): 
    :technician (optional): 
    :returned (optional): 
    :under_warranty (optional): 
    :parts_replaced (optional): 
    :device_replaced (optional): 
    :serviced_by (optional): 
    :service_contract (optional): 
    :service_document (optional): 
    :responsible (optional): 
    :description (optional): Description
    :private (optional): Is it private Boolean
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 

    """

    # General Fields
    issue = models.CharField(max_length=64, blank=True, null=True, verbose_name="Service Issue")
    resolution = models.CharField(max_length=64, blank=True, null=True, verbose_name="Service Resolution")
    work_done = models.CharField(max_length=64, blank=True, null=True, verbose_name="Work Done")
    left_inventory = models.CharField(max_length=16, blank=True, null=True, verbose_name="Date Left Inventory")
    return_date = models.CharField(max_length=16, blank=True, null=True, verbose_name="Date Returned to Inventory")
    cost = models.CharField(max_length=45, blank=True, null=True, verbose_name="Service Cost")
    technician = models.CharField(max_length=64, blank=True, null=True, verbose_name="Repair Technician")
    returned = models.BooleanField(default=False, verbose_name="Device Returned to Inventory")
    under_warranty = models.BooleanField(default=True, verbose_name="Under Warranty")
    parts_replaced = models.BooleanField(default=False, verbose_name="Parts Replaced")
    device_replaced = models.BooleanField(default=False, verbose_name="Device Replaced")

    # Linked Fields
    serviced_by = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Serviced By")
    service_contract = models.ForeignKey(ServiceContract, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Service Contract")
    #service_document = models.CharField(max_length=64, blank=True, null=True, verbose_name="Service Document")
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='responsible_for_service',
                                    on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Resposnsible Party")

    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return self.issue

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Service History')


class Comment(ObjectDescriptionMixin):
    """
    Model to contain information about a device comment.

    :text (optional): 
    :device (optional): 
    :user (optional): 
    :private (optional): Is it private Boolean
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 

    """

    # General Fields
    text = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Comment')

    # Linked Fields
    device = models.ForeignKey(Device, related_name='comment_device', on_delete=models.CASCADE, verbose_name='Comment Device')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_user', on_delete=models.CASCADE, verbose_name='Comment User')
    
    # Auto Fields   
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Device Comment')
        verbose_name_plural = _('Device Comments')

    def save(self,force_insert=False, force_update=False):
        models.Model.save(self,force_insert,force_update)
