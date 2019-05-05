## Inventory Models ##

# python imports
import itertools
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from simple_history.models import HistoricalRecords
from utils.choices import DEVICE_STATUS_CHOICES
from utils.choices import DEVICE_CONDITION_CHOICES
from utils.choices import DEVICE_SERVICE_STATUS_CHOICES
from utils.models import ObjectDescription
from utils.models import Authorisation
from utils.models import BaseObject
from utils.models import Note
from entity.models.company import Company
from entity.models.person import Person
#import case.managers as managers
#from note.models import Note


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


## Admin Models
class DeviceCategory(BaseObject):
    """  Model to contain information about a device category.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        category (DeviceCategory): Categories
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
        verbose_name = _('Device Category')
        verbose_name_plural = _('Device Categories')


class DeviceSubcategory(BaseObject):
    """  Model to contain information about a device classification.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        category (DeviceCategory): Categories
        title (str) [50]: Title
        colour (str, optional) [7]: Hexidecimal colour representation
        description (str, optional) [1000]: Description
        created (date, auto): Date Created
        modified (date,auto): Date Modified
        created_by (User, auto): Created by
        modified_by (User, auto): Modified by 
    
    """
    
    # Linked Fields
    category = models.ForeignKey(
		DeviceCategory, 
		on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='category', 
		verbose_name=_("Device Category"),
		help_text=_("Device Category"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Device Subcategory')
        verbose_name_plural = _('Device Subcategories')


class ServiceContract(ObjectDescription):
    """  Model to contain information about a device service contract.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        title (str) [128] : Title
        internal_id (str, optional) [45]: Internal ID
        service_id (str, optional) [45]: Service Contract Reference
        terms (str, optional) [None]: Terms of Contract
        contract_start (Date, optional): Duration of Contract
        contract_end (Date, optional): Renewal Date
        renewal_cost (float, optional) [12.2] : Renewal Cost
        active (bool, optional): Is active
        vendor (Company, optional): Vendor
        contact (Person, optional): Vendor Contact
        document (File, optional): Document Upload
        responsible (User, optional): Staff Responsible
        description (str, optional) [1000]: Description
        created (date, auto): Date Created
        modified (date,auto): Date Modified
        created_by (User, auto): Created by
        modified_by (User, auto): Modified by 

    """

    # General Fields
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        default=None,
        verbose_name=_("Title"),
        help_text=_("Enter a title for the Service Contract"))

    internal_id = models.CharField(
        max_length=45, 
        blank=True, 
        null=True, 
        verbose_name=_("Internal ID"),
        help_text=_("Enter the internal id for the Service Contract"))

    service_id = models.CharField(
        max_length=45, 
        blank=True, 
        null=True, 
        verbose_name=_("Service ID"),
        help_text=_("Enter a contract id for the Service Contract"))

    terms = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_("Terms and Conditions"),
        help_text=_("Enter the terms for the Service Contract"))
    
    contract_start = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_("Contract Duration"),
        help_text=_("Enter a duration for the Service Contract"))

    contract_end = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_("Renewal Date"),
        help_text=_("Enter a renewal date for the Service Contract"))

    renewal_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name=_("Renewal Cost"),
        help_text=_("Enter the renewal cost for the Service Contract"))

    active = models.BooleanField(
        default=False, 
        blank=True, 
        verbose_name=_("Active"),
        help_text=_("(Optional) Is Contract Active"))

    # Linked Fields
    vendor = models.ForeignKey(
        Company,
        on_delete=models.DO_NOTHING,
        blank=True, 
        related_name=_('service_contract_vendor'),
        verbose_name=_("Contract Vendor"),
        help_text=_("Enter the vendor for the Service Contract"))

    contact = models.ForeignKey(
        Person,
        on_delete=models.DO_NOTHING,
        blank=True, 
        related_name=_('service_contract_contact'),
        verbose_name=_("Contract Contact"),
        help_text=_("Enter the contact for the Service Contract"))

    #document = models.FileField(
    #    upload_to='uploads/' ,
    #    blank=True, 
    #    null=True,
    #    verbose_name=_("File Upload"),
    #    help_text=_("Upload the Service Contract"))

    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        related_name=_('service_sontract_responsible'), 
        verbose_name=_("Resposnsible Party"),
        help_text=_("Enter the resposnsible party for the Service Contract"))

    # Auto Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Service Contract')
        verbose_name_plural = _('Service Contracts')

    def __str__(self):
        """ Returns a human friendly string
        
        Returns:
            Title

        """
        return '%s' % _(self.title)


## Main Models
class Device(ObjectDescription):
    """  Model to contain information about a device
 
    Args:
        history (HistoricalRecord, auto): Historical records of object
        title (str) [128] : Title 
        model (str, optional) [128] : Model 
        manufacturer (str, optional) [128] : Manufacturer 
        variation (str, optional) [128] : Variation 
        serial_number (str, optional) [128] : Serial Number  
        status (DEVICE_STATUS_CHOICES, optional) [2] : Device Status 
        condition (DEVICE_CONDITION_CHOICES, optional) [2] : Device Condition 
        returnable (Boolean, optional) : Item is Returnable 
        internal_id (str, optional) [45] : Internal ID
        model_number (str, optional) [45] : Model Number 
        purchased (Date, optional) : Date Purchased
        manual (FileUpload, optional) : Device Manual Upload
        warranty_title (str, optional) [128]: Warranty Title
        warranty_id (str, optional) [45] : Reference ID
        warranty_terms (str, optional) [None] : Warranty Terms
        warranty_duration (Date, optional) : Warranty Duration
        warranty_start (Date, optional) : Warranty Start Date 
        warranty_end (Date, optional) : Warranty End Date
        warranty_extended (Boolean, optional) : Extended Warranty 
        warranty_document (FileUpload, optional) : Warranty Document 
        warranty_contact (Person, optional) : Warranty Contact
        warranty_vendor (Company, optional) : Warranty Vendor
        warranty_responsible (User, optional) : Staff Responsible for Warranty
        sales_rep (Person, optional) : Sales Rep
        vendor (Company, optional) : Vendor
        service_contract (Service Contract, optional) : Service Contract
        subcategory (DeviceSubcategory, optional): Device Subcategory
        category (DeviceCategory, optional) : Device Category
        authorisation (Authorisation, optional) : Device Authorisation
        manager (User, optional) : Device Manager
        device_dependency (Device, optional) : Device Dependacies
        related_devices (Device, optional) : Related Devices
        description (str, optional) [1000] : Description
        created (date, auto) : Date Created
        modified (date,auto) : Date Modified
        created_by (User, auto) : Created by
        modified_by (User, auto) : Modified by 
        slug (slug, Auto): Slug of title

    Methods:
        check_in (Object) : Changes status and saves object
        check_out (Object) :  Changes status to 'CHECKED_OUT' and saves object

    """

    ## General Fields ##
    title = models.CharField(
        max_length=128, 
        null=True, 
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Enter a title for the Device"))

    model = models.CharField(
        max_length=128, 
        null=True, 
        blank=True,
        verbose_name=_("Device Model"),
        help_text=_("Enter a model for the Device"))
        
    manufacturer = models.CharField(
        max_length=128, 
        blank=True, 
        null=True,
        verbose_name=_("Device Manufacturer"),
        help_text=_("Enter the Manufacturer"))

    variation = models.CharField(
        max_length=128, 
        null=True, 
        blank=True, 
        verbose_name=_("Device Variation"),
        help_text=_("Enter a varitaion of the Device"))

    serial_number = models.CharField(
        max_length=128, 
        null=True, 
        blank=True, 
        verbose_name=_("Serial Number"),
        help_text=_("Enter the serial number of the Device"))

    status = models.CharField(
        max_length=2, 
        choices=DEVICE_STATUS_CHOICES, 
        verbose_name=_("Device Status"),
        help_text=_("Select the status of the Device"))

    condition = models.CharField(
        max_length=2, 
        choices=DEVICE_CONDITION_CHOICES, 
        verbose_name=_("Device Condition"),
        help_text=_("Select the condition of the Device"))

    returnable = models.BooleanField(
        default=True, 
        verbose_name=_("Returnable To Stock"), 
        help_text=_("Is the Device returnable To stock"))

    internal_id = models.CharField(
        max_length=45, 
        blank=True, 
        null=True, 
        verbose_name=_("Internal ID"),
        help_text=_("Enter the internal id of the Device"))

    model_number = models.CharField(
        max_length=45, 
        blank=True, 
        null=True, 
        verbose_name=_("Model Number"),
        help_text=_("Enter the model number of the Device"))

    purchased = models.DateField(
        blank=True, 
        null=True,
        default=timezone.now,
        verbose_name=_('Purchase Date'),
        help_text=_("Enter the date the Device was purchased"))

    #manual = models.FileField(
    #    upload_to='uploads/', 
    #    blank=True, 
    #    null=True,
    #    verbose_name=_("Manual Upload"),
    #    help_text=_("Upload the Manual for the Device"))

    warranty_title = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        verbose_name=_("Warranty Title"),
        help_text=_("Enter the internal id of the Warranty"))

    warranty_duration = models.CharField(
        max_length=16, 
        blank=True, 
        null=True, 
        verbose_name=_("Warranty Duration"),
        help_text=_("Enter the duration of the Warranty"))

    warranty_id = models.CharField(
        max_length=45, 
        blank=True, 
        null=True, 
        verbose_name=_("Warranty Reference ID"),
        help_text=_("Enter the reference id of the Warranty"))

    warranty_terms = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_("Warranty Terms and Conditions"),
        help_text=_("Enter the terms and conditions of the Warranty"))

    warranty_start = models.DateField(
        blank=True, 
        null=True,
        default=timezone.now,
        verbose_name=_('Warranty Start Date'), 
        help_text=_("Enter the start date of the Warranty"))

    warranty_end = models.DateField(
        blank=True, 
        null=True,
        default=timezone.now,
        verbose_name=_('Warranty End Date'), 
        help_text=_("Enter the end date of the Warranty"))

    warranty_extended = models.BooleanField(
        default=False, 
        verbose_name=_("Extended Warranty"),
        help_text=_("Has the Warranty been extended"))

    #warranty_document = models.FileField(
    #    upload_to='uploads/',
    #    blank=True, 
    #    null=True,
    #    verbose_name=_("File Upload"),
    #    help_text=_("Upload the Warranty Contract"))


    ## Linked Fields ##
    warranty_contact = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name=_('warranty_contact'),
        verbose_name=_("Warranty Contact"),
        help_text=_("Select the vendor contact for the Warranty"))

    warranty_responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name=_('warranty_resposible'), 
        verbose_name=_("Warranty Responsible"),
        help_text=_("Select the staff resposnible for the Warranty"))

    warranty_vendor = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name=_('warranty_vendor'), 
        verbose_name=_("Warranty Vendor"),
        help_text=_("Select the vendor for the Warranty"))

    sales_rep = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name=_('sales_rep'),
        verbose_name=_("Vendor Sales Rep"),
        help_text=_("Select the Sales Representative"))

    vendor = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name=_('device_vendor'),
        verbose_name=_("Device Vendor"),
        help_text=_("Select the Device Vendor"))

    service_contract = models.ForeignKey(
        ServiceContract, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name=_('device_service_contract'),
        verbose_name=_("Device Service Contract"),
        help_text=_("Select the Service Contract"))

    subcategory = models.ForeignKey(
        DeviceSubcategory, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name=_('device_subcategory'),
        verbose_name=_("Device Subcategory"),
        help_text=_("Select the Device Subcategory"))

    category = models.ForeignKey(
        DeviceCategory, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name=_('device_category'),
        verbose_name=_("Device Category"),
        help_text=_("Select the Device Category"))

    authorisation = models.ForeignKey(
        Authorisation, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name=_('device_authorisation'),
        verbose_name=_("Device Authorisation"),
        help_text=_("Select the Device Autorisation Level"))

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name=_('device_manager'), 
        verbose_name=_("Device Manager"),
        help_text=_("Select the Device Manager"))
    
    #device_dependency = models.ManyToMany(
    #    Device, 
    #    related_name=_('device_dependecies'), 
    #    verbose_name=_("Device Dependency"),
    #    help_text=_("Select the Device Dependencies"))

    #related_devices = models.ManyToMany(
    #    Device,
    #    related_name=_('related_devices'),  
    #    verbose_name=_("Related Devices"),
    #    help_text=_("Select Related Devices"))
        
    # Auto Fields
    slug = models.SlugField(
        editable=False, 
        null=True, 
        blank=True, 
        verbose_name=_("Device Slug"),
        help_text=_("Enter the Device slug"))
    
    history = HistoricalRecords()  

    class Meta:
        #permissions = (
        #    ('can_change_device_status', "Can change device status"),
        #    ('can_update_device_attributes', "Can update device attributes")
        #)
        #get_latest_by = 'created_at'
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

    def __str__(self):
        """ Returns a human friendly string
        
        Returns:
            Title

        """
        return '%s' % _(self.title)
    
    def get_absolute_url(self):
        """ Returns a url of object
        
        Returns:
            device_detail

        """
        if not (self.slug):
            self.save(force_update=True)
        return reverse('device_detail',args=[self.pk])

    def check_in(self, condition='excellent'):
        """ Changes status and saves object

        Args:
            condition (str) [2] : The item condition

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
        """ Changes status to 'CHECKED_OUT' and saves object

        """
        self.status = Device.CHECKED_OUT
        return self.save()

    def save(self,force_insert=False, force_update=False):
        """ Saves the Object.
                if new object;
                    sets the 'created' to the current time
                    sets the 'created_by' to the current user
                if existing object;
                    sets the 'modified' to the current time
                    sets the 'modified_by' to the current user
                if a slug does not exist;
                    sets 'slug' to slug of 'title'
        
        Returns:
            The new Object

        """
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


class Service(ObjectDescription):
    """ Model to contain information about a device service.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        issue (str) [None] : Issue
        resolution (str, optional) [None] : Resolution 
        status (DEVICE_STATUS_CHOICES, optional) [2] : Service Status 
        technician (str, optional) [128] : 
        leave_date (Date, optional) : Date Left Inventory
        return_date (Date, optional) : Date Returned to Inventory
        cost (Float, optional) [12.2] : Service Cost
        invoice (File, optional): Invoice Upload
        receipt (File, optional): Receipt Upload
        returned (Boolean, optional): Device Returned
        under_warranty (Boolean, optional): Under Warranty
        tested (Boolean, optional): Tested
        vendor (Company, optional): Vendor Serviced By
        service_contract (ServiceContract, optional): Service Contract
        manager (User, optional): Service Manager
        tested_by (User, optional): Tested By
        description (str, optional) [1000]: Description
        created (date, auto): Date Created
        modified (date,auto): Date Modified
        created_by (User, auto): Created by
        modified_by (User, auto): Modified by 

    """

    ## General Fields ##
    issue = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_("Issue"),
        help_text=_("Enter the issue"))

    resolution = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_("Resolution"),
        help_text=_("Enter the resolution"))

    status = models.CharField(
        max_length=2, 
        choices=DEVICE_SERVICE_STATUS_CHOICES, 
        verbose_name=_("Service Status"),
        help_text=_("Select the sservice status"))

    technician = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        verbose_name=_("Repair Technician"),
        help_text=_("Enter the service techncician's name"))

    leave_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_("Date Left Inventory"),
        help_text=_("Enter the date left for service"))

    return_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_("Date Returned to Inventory"),
        help_text=_("Enter the return date to inventory"))

    cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name=_("Service Cost"),
        help_text=_("Enter the service cost"))

    #invoice = models.FileField(
    #    blank=True, 
    #    null=True,
    #    upload_to='uploads/' 
    #    verbose_name=_("Invoice Upload"),
    #    help_text=_("Upload the Invoice"))

    #receipt = models.FileField(
    #    blank=True, 
    #    null=True,
    #    upload_to='uploads/' 
    #    verbose_name=_("Receipt Upload"),
    #    help_text=_("Upload the Receipt"))

    returned = models.BooleanField(
        default=False, 
        verbose_name=_("Returned to Inventory"),
        help_text=_("Device returned"))

    under_warranty = models.BooleanField(
        default=True, 
        verbose_name=_("Under Warranty"),
        help_text=_("Device under warranty"))
    
    tested = models.BooleanField(
        default=True, 
        verbose_name=_("Tested By"),
        help_text=_("Device tested upon return"))

    ## Linked Fields ##
    vendor = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name=_('serviced_by'),
        verbose_name=_("Serviced By"),
        help_text=_("Select the Service Vendor"))

    service_contract = models.ForeignKey(
        ServiceContract, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name=_('service_service_contract'),
        verbose_name=_("Service Contract"),
        help_text=_("Select the Service Contract"))

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name=_('service_manager'),
        verbose_name=_("Manager"),
        help_text=_("Select the Service manager"))

    tested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name=_('tested_by'),
        verbose_name=_("Tested By"),
        help_text=_("Select who tested the device upon return"))

    ## Auto Fields ##
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Service History')
        verbose_name_plural = _('Service History')

    def __str__(self):
        """ Returns a human friendly string
        
        Returns:
            Issue

        """
        return '%s' % _(self.issue)
