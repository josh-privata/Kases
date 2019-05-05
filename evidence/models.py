## Evidence Models ##

## python imports
import itertools
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from utils.models import ObjectDescription
from utils.models import Authorisation
from utils.models import Priority
from utils.models import BaseObject
from utils.models import Note
#import evidence.managers as managers


## Admin Models
class EvidenceCategory(BaseObject):
	""" Model to contain information about evidence category.

	Args:
		history (HistoricalRecord, auto): Historical records of object
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
		verbose_name = _('Evidence Category')
		verbose_name_plural = _('Evidence Categories')


class EvidenceStatus(BaseObject):
	""" Model to contain information about evidence status.

	Args:
		history (HistoricalRecord, auto): Historical records of object
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
		verbose_name = _('Evidence Status')
		verbose_name_plural = _('Evidence Status')


class EvidenceStatusGroup(BaseObject):
	""" Model to contain information about evidence status group.

	Args:
		status (EvidenceStatus): Status in group
		history (HistoricalRecord, auto): Historical records of object
		title (str) [50]: Title
		colour (str, optional) [7]: Hexidecimal colour representation
		description (str, optional) [1000]: Description
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified by
	
	"""

	# Linked Fields
	status = models.ManyToManyField(
		EvidenceStatus, 
		blank=True, 
		verbose_name=_("Evidence Status"),
		help_text=_("Select Evidence Status"))
	
	history = HistoricalRecords()

	class Meta:
		verbose_name = _('Evidence Status Group')
		verbose_name_plural = _('Evidence Status Groups')


## Main Models
class ChainOfCustody(ObjectDescription):
	""" Model to contain information about evidence chain of custody.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		description (str, optional) [1000]: Description
		receipt (str, optional) [50]: Receipt number
		date_of_receipt (date, optional): Date of custody
		check_in (boolean, optional): Is checked-in
		custodian (AUTH_USER_MODEL, optional): Custodian
		assigned_by (AUTH_USER_MODEL, optional): Assigned To
		assigned_to (AUTH_USER_MODEL, optional): Assigned By
		private (bool, optional): Is private
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified by
	
	"""

	## General Fields ##
	receipt = models.CharField(
		max_length=50, 
		blank=True, 
		null=True, 
		default=None, 
		verbose_name=_("Custody Receipt Number"),
		help_text=_("(Optional) Enter reciept number"))

	date_of_receipt = models.DateTimeField(
		auto_now=False, 
		null=True, 
		default=timezone.now,
		verbose_name=_("Date of Custody"),
		help_text=_("(Optional) Enter date of reciept"))

	check_in = models.BooleanField(
		default=False,
		blank=True, 
		verbose_name=_("Checked-In"),
		help_text=_("(Optional) Is the item recieved"))

	## Linked Fields ##
	custodian = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		blank=True, 
		null=True,
		related_name='chain_of_custody_custodian', 
		verbose_name=_("Evidence Custodian"),
		help_text=_("(Optional) Select the Chain Of Custody Custodian"))

	assigned_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		blank=True, 
		null=True,
		related_name='chain_of_custody_assigned_by', 
		verbose_name=_("Assigned By"),
		help_text=_("(Optional) Select Chain Of Custody assigned by"))

	assigned_to = models.ManyToManyField(
		settings.AUTH_USER_MODEL, 
		blank=True,
		related_name='chain_of_custody_assigned_to', 
		verbose_name=_("Assigned To"),
		help_text=_("(Optional) Select Chain Of Custody assigned to"))
	
	history = HistoricalRecords()

	class Meta:
		verbose_name = _('Chain Of Custody')
		verbose_name_plural = _('Chain Of Custody')

	def __str__(self):
		""" Returns a human friendly string
		
		Returns:
			Title

		"""
		return '%s' % _(self.description)


class Evidence(ObjectDescription):
	""" Abstract model to contain information about evidence.

	Args:
		title (str) [128]: Evidence title
		reference (str, optional) [45]: Reference code
		bag_number (str, optional) [45]: Bag number
		location (str, optional) [250]: Location of the evidence
		file_location (file, optional): Location for evidence file
		image_upload (file, optional): Location for the evidence image
		qr_code (str, optional) [128]: QR Code 
		retention_reminder_sent (boolean, optional): Retention reminder sent
		retention_start_date (date, optional): Retention start date
		retention_end_date (date, optional): Retention end date
		chain_of_custody (ChainOfCustody, optional): Chain of custody
		status (EvidenceStatus, optional): Status of the Evidence
		priority (Priority, optional): Priority of the Evidence
		authorisation (Authorisation, optional): Authorisation of the Evidence
		custodian (AUTH_USER_MODEL, optional): Evidence custodian
		assigned_by (AUTH_USER_MODEL, optional): Assigned To
		assigned_to (AUTH_USER_MODEL, optional): Assigned By
		note (Note, optional): Notes relating to the Evidence
		description (str, optional) [1000]: Description
		private (bool, optional): Is private
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified by
		slug (slug, auto): Slug of title
	
	"""

	## General Fields ##
	title = models.CharField(
		max_length=128,
		blank=False,
		null=False,
		default=None,
		verbose_name=_("Title"),
		help_text=_("Enter a title for the Evidence"))

	reference = models.CharField(
		max_length=45, 
		blank=True, 
		null=True, 
		default=None, 
		verbose_name=_("Reference"),
		help_text=_("Enter a reference code for the Evidence"))

	bag_number = models.CharField(
		max_length=50, 
		blank=True,
		null=True, 
		default=None, 
		verbose_name=_("Bag Number"),
		help_text=_("Enter a bag number for the Evidence"))

	location = models.CharField(
		max_length=250, 
		blank=True, 
		null=True, 
		default=None, 
		verbose_name=_("Location"),
		help_text=_("Enter a current location for the Evidence"))

	file_location = models.FileField(
		upload_to='',
		blank=True, 
		null=True, 
		verbose_name=_("File Location"),
		help_text=_("Upload a file location for the Evidence"))

	image_upload = models.FileField(
		upload_to='',
		blank=True, 
		null=True, 
		verbose_name=_("Image"),
		help_text=_("Upload an image for the Evidence"))

	qr_code = models.CharField(
		max_length=128, 
		blank=True, 
		null=True, 
		default=None, 
		verbose_name=_("QR Code"),
		help_text=_("Enter a QR code for the evidence"))

	retention_reminder_sent = models.BooleanField(
		default=False, 
		blank=True, 
		verbose_name=_("Retention Reminder"),
		help_text=_("Has a rentention reminder been sent"))

	retention_start_date = models.DateTimeField(
		auto_now=False, 
		blank=True,
		null=True, 
		default=timezone.now,
		verbose_name=_("Retention Start Date"),
		help_text=_("Enter the retention start date"))
	
	retention_end_date = models.DateTimeField(
		auto_now=False, 
		blank=True, 
		null=True, 
		verbose_name=_("Retention End Date"),
		help_text=_("Enter the retention end date"))


	## Linked Fields ##  
	category = models.ForeignKey(
		EvidenceCategory, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True, 
		verbose_name=_("Evidence Category"),
		help_text=_("(Optional) Select the category of Evidence"))

	status = models.ForeignKey(
		EvidenceStatus, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		verbose_name=_("Status"),
		help_text=_("(Optional) Select the status of the Evidence"))

	priority = models.ForeignKey(
		Priority, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		verbose_name=_("Priority"),
		help_text=_("(Optional) Select the priority of the Evidence"))

	authorisation = models.ForeignKey(
		Authorisation, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		verbose_name=_("Authorisation"),
		help_text=_("(Optional) Select the authorisation of the Evidence"))

	custodian = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		blank=True, 
		null=True,
		related_name='evidence_custodian', 
		verbose_name=_("Evidence Custodian"),
		help_text=_("(Optional) Select the Evidence Custodian"))

	assigned_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		blank=True, 
		null=True,
		related_name='evidence_assigned_by', 
		verbose_name=_("Assigned By"),
		help_text=_("(Optional) Select Evidence assigned by"))

	assigned_to = models.ManyToManyField(
		settings.AUTH_USER_MODEL, 
		blank=True,
		related_name='evidence_assigned_to', 
		verbose_name=_("Assigned To"),
		help_text=_("(Optional) Select Evidence assigned to"))

	note = models.ManyToManyField(
		Note, 
		blank=True, 
		related_name='evidence_note', 
		verbose_name=_("Note"),
		help_text=_("(Optional) Enter a note relating to the Evidence"))
	
	chain_of_custody = models.ManyToManyField(
		ChainOfCustody, 
		blank=True, 
		verbose_name=_("Chain Of Custody"),
		help_text=_("(Optional) Enter the chain of custody"))

	## Auto Fields ##
	slug = models.SlugField(
		blank=True, 
		null=True, 
		unique=True, 
		verbose_name=_("Slug"),
		help_text=_("A slug value representing title"))

	class Meta:
		abstract = True

	def __str__(self):
		""" Returns a human friendly string
		
		Returns:
			Title

		"""
		return '%s' % _(self.title)
