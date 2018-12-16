## Loan Models ##

# python imports
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from simple_history.models import HistoricalRecords
from utils.models import ObjectDescription
#import loan.managers as managers
from case.models import Case
from case.models import CaseInventory
from inventory.models import Device
from utils.choices import LOAN_STATUS_CHOICES
from utils.choices import DEVICE_STATUS_CHOICES
from utils.choices import DEVICE_CONDITION_CHOICES


class Loan(ObjectDescription):
	"""
	Model to contain information about a loan.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		approver_note (str, optional) [1000] : Approver Note
		return_note (str, optional) [1000] : Return Note
		booked_from (Date, optional) : Booked From
		booked_until (Date, optional) : Booked To
		date_taken (Date, optional) : Date Taken
		date_returned (Date, optional) : Date Returned
		original_condition (str, optional) [2] : Original Condition
		return_condition (str, optional) [2] : Return Condition
		status (str, optional) [2] : Loan Status
		returned (boolean, optional) : Has Been Returned
		taken (boolean, optional) : Has Been Taken
		case (Case) : Case
		device (Device) : Device
		loaned_to (User, optional) : Loaned To
		loaned_by (User, optional) : Loaned By
		taken_by (User, optional) : Taken By
		returned_by (User, optional) : Returned By
		private (bool, optional) : Is private
		description (str, optional) [1000] : Description
		created (date, auto) : Date Created
		modified (date,auto) : Date Modified
		created_by (User, auto) : Created by
		modified_by (User, auto) : Modified by

	"""
	
	## General Fields ##
	approver_note = models.TextField(
		max_length=1000, 
		null=True, 
		blank=True, 
		verbose_name=_('Approver Note'),
		help_text=_("Enter an approver's note"))

	return_note = models.TextField(
		max_length=1000, 
		null=True, 
		blank=True, 
		verbose_name=_('Return Note'),
		help_text=_("Enter a return note"))

	booked_from = models.DateField(
		null=True, 
		blank=True, 
		verbose_name=_('Booked From'),
		help_text=_("Enter the booked from date"))

	booked_until = models.DateField(
		null=True, 
		blank=True, 
		verbose_name=_('Booked Until'),
		help_text=_("Enter the booked until date"))

	date_taken = models.DateField(
		null=True, 
		blank=True, 
		verbose_name=_('Date Taken'),
		help_text=_("Enter the date taken"))

	date_returned = models.DateField(
		null=True, 
		blank=True, 
		verbose_name=_('Date Returned'),
		help_text=_("Enter the date returned"))

	original_condition = models.CharField(
		max_length=2, 
        null=True, 
		blank=True,
		choices=DEVICE_CONDITION_CHOICES, 
		verbose_name=_("Original Condition"),
		help_text=_("Select the original condition"))

	return_condition = models.CharField(
		max_length=2,
        null=True, 
		blank=True,
		choices=DEVICE_CONDITION_CHOICES, 
		verbose_name=_("Returned Condition"),
		help_text=_("Select the returned condition"))

	status = models.CharField(
		max_length=2,
        null=True, 
		blank=True,
		choices=LOAN_STATUS_CHOICES, 
		verbose_name=_("Status"),
		help_text=_("Select the loan status"))

	returned = models.BooleanField(
		default=False, 
		verbose_name=_("Returned"),
		help_text=_("Device returned"))

	taken = models.BooleanField(
		default=False, 
		verbose_name=_("Taken"),
		help_text=_("Device taken"))

	## Linked Fields ##
	case = models.ForeignKey(
		Case, 
		on_delete=models.DO_NOTHING, 
		blank=True, 
		related_name=_('loan_case'), 
		verbose_name=_("Case"),
		help_text=_("Select the case"))

	device = models.ForeignKey(
		Device, 
		on_delete=models.DO_NOTHING, 
		blank=True, 
		related_name=_('loan_device'),
		verbose_name=_("Device"),
		help_text=_("Select the device"))

	loaned_to = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.DO_NOTHING, 
		blank=True, 
		null=True, 
		related_name=_('loaned_to'),
		verbose_name=_("Loaned To"),
		help_text=_("Select who the device is loaned to"))

	loaned_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.DO_NOTHING,
		blank=True,
		null=True,
		related_name=_('loaned_by'),
		verbose_name=_("Loaned By"),
		help_text=_("Select who the device is loaned by"))
	
	returned_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.DO_NOTHING, 
		blank=True, 
		null=True, 
		related_name=_('returned_by'),
		verbose_name=_("Returned By"),
		help_text=_("Select who the device was returned by"))

	taken_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.DO_NOTHING,
		blank=True,
		null=True,
		related_name=_('taken_by'),
		verbose_name=_("Taken By"),
		help_text=_("Select who the device was taken by"))

	## Auto Fields ##

	history = HistoricalRecords()
	
	class Meta:
		verbose_name = _('Device Loan')
		verbose_name_plural = _('Device Loans')

	def get_absolute_url(self):
		return reverse('loan_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return '%s - %s' % (_(self.case), _(self.device))

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

		# LOAN_CLOSED = 'LC'
		if self.status == 'LC':

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
