## Case Models ##

## python imports
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
from utils.choices import ENTITY_TYPE_CHOICES
from inventory.models import Device
from event.models import Event
from task.models import Task
from evidence.models import Evidence
from entity.models.person import Person
from entity.models.company import Company
#import case.managers as managers

## Admin Models
class CaseClassification(BaseObject):
	""" Model to contain information about a case classification.

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
		verbose_name = _('Case Classification')
		verbose_name_plural = _('Case Classifications')


class CaseType(BaseObject):
	""" Model to contain information about a case type.

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
		verbose_name = _('Case Type')
		verbose_name_plural = _('Case Types')


class CasePriority(Priority):
	"""  Model to contain information about a case priority.

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
		verbose_name = _('Case Priority')
		verbose_name_plural = _('Case Priorities')


class CaseCategory(BaseObject):
	""" Model to contain information about a case category.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		title (str) [50]: Title
		colour (str, optional) [7]: Hexidecimal colour representation
		delta (int, optional): Time delta
		description (str, optional) [1000]: Description
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified by 
	
	"""

	history = HistoricalRecords()

	class Meta:
		verbose_name = _('Case Category')
		verbose_name_plural = _('Case Categories')


class CaseStatus(BaseObject):
	""" Model to contain information about a case status.

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
		verbose_name = _('Case Status')
		verbose_name_plural = _('Case Status')


class CaseStatusGroup(BaseObject):
	""" Model to contain information about a case status group.

	Args:
		status (EventStatus): Status in group
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
		CaseStatus, 
		blank=True, 
		verbose_name=_("Case Status"),
		help_text=_("Select Case Status"))

	history = HistoricalRecords()

	class Meta:
		verbose_name = _('Case Status Group')
		verbose_name_plural = _('Case Status Groups')


## Main Models
class Case(ObjectDescription):
	""" Model to contain information about a case.

	Args:
        history (HistoricalRecord, auto): Historical records of object
		title (str) [250] : Title
		reference (str, optional) [45] : Reference
		description (str, optional) [None] : Description
		background (str, optional) [None] : Background
		purpose (str, optional) [2500] : Purpose
		deadline (Date, optional) : Deadline
		image_upload (FileField, optional) : Image Upload 
		note (Note, optional) : Note
		type (Type, optional) : Type
		status (Status, optional) : Status
		classification (Classification, optional) : Classification
		priority (Priority, optional) : Priority
		category (Category, optional) : Category
		authorisation (Authorisation, optional) : Authorisation
		assigned_to (User, optional) : Assigned To
		assigned_by (User, optional) : Assigned By
		manager (User, optional) : Case Manager
		judge (Person, optional) : Representing Judge
		private (bool, optional): Is private
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified by
		slug (slug, auto): Slug of title    

	Methods:
		get_url (URL) : Gets Case edit url
		_get_assigned_to (User) : Check for 'unassigned' or assigned to
		_get_case (URL) : a combination of Case ID and queue slug.
		_get_case_for_url (URL) : A URL-friendly Case ID, used in links.

	"""

	# General Fields
	title = models.CharField(
		max_length=350,
		blank=False,
		null=False,
		verbose_name=_("Title"),
		help_text=_("Enter a title for the Case"))

	reference = models.CharField(
		max_length=45, 
		blank=True, 
		null=True, 
		verbose_name=_("Reference"),
		help_text=_("Enter a reference code for the Case"))

	description = models.TextField(
		blank=True, 
		null=True, 
		verbose_name=_("Case Description"),
		help_text=_("Enter a description for the Case"))

	background = models.TextField(
		blank=True, 
		null=True, 
		verbose_name=_("Case Background"),
		help_text=_("Enter a background for the Case"))
	
	purpose = models.CharField(
		max_length=2500, 
		blank=True, 
		null=True, 
		verbose_name=_("Case Purpose")    ,
		help_text=_("Enter a purpose for the Case"))
	
	#deadline = models.DateField(
	#    auto_now=False, 
	#    null=True, 
	#    verbose_name=_("Deadline"),
	#    help_text=_("Enter a deadline for the Case"))

	image_upload = models.FileField(
		upload_to='uploads/',
		blank=True, 
		null=True, 
		verbose_name=_("Image"),
		help_text=_("Upload an image for the Case"))

	# Linked Fields
	#note = models.ManyToManyField(
	#    Notes, 
	#    on_delete=models.DO_NOTHING, 
	#    blank=True, 
	#    null=True,
	#    related_name=_('case_note'),
	#    verbose_name=_("Case Note")
	#    help_text=_("Select a judge"))

	type = models.ForeignKey(
		CaseType, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		related_name=_('case_type'),
		verbose_name=_("Case Type"),
		help_text=_("Select a case type"))

	status = models.ForeignKey(
		CaseStatus, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		related_name=_('case_status'),
		verbose_name=_("Case Status"),
		help_text=_("Select a case status"))

	classification = models.ForeignKey(
		CaseClassification, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		related_name=_('case_classification'),
		verbose_name=_("Case Classification"),
		help_text=_("Select a case classification"))

	priority = models.ForeignKey(
		CasePriority, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True, 
		related_name=_('case_priority'),
		verbose_name=_("Case Priority"),
		help_text=_("Select a case priority"))

	category = models.ForeignKey(
		CaseCategory, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		related_name=_('case_category'),
		verbose_name=_("Case Category"),
		help_text=_("Select a case category"))

	authorisation = models.ForeignKey(
		Authorisation, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		related_name=_('case_authorisation'),
		verbose_name=_("Case Authorisation"),
		help_text=_("Select a case authorisation"))

	assigned_to = models.ManyToManyField(
		settings.AUTH_USER_MODEL, 
		related_name=_('case_assigned_to'),
		verbose_name=_("Assigned To"),
		help_text=_("Select assigned to"))

	assigned_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		blank=True, 
		null=True, 
		related_name=_('case_assigned_by'),
		verbose_name=_("Assigned By"),
		help_text=_("Select assigned by"))

	manager = models.ForeignKey(
		settings.AUTH_USER_MODEL,  
		on_delete=models.CASCADE, 
		blank=True, 
		null=True,
		related_name=_('case_manager'),
		verbose_name=_("Case Manager"),
		help_text=_("Select a case manager"))

	#judge = models.ForeignKey(
	#    Person, 
	#    on_delete=models.CASCADE, 
	#    blank=True, 
	#    null=True,
	#    related_name=_('case_judge'),
	#    verbose_name=_("Judge"),
	#    help_text=_("Select a judge"))
	
	# Auto Fields
	slug = models.SlugField(
		blank=True, 
		null=True, 
		unique=True, 
		verbose_name=_("Slug"),
		help_text=_("A slug value representing title"))

	history = HistoricalRecords()

	#manager = CaseManager()

	class Meta:
		verbose_name = _('Case')
		verbose_name_plural = _('Cases')

	def get_absolute_url(self):
		return reverse('case_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return '%s' % self.title
	
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

	def save(self,force_insert=False, force_update=False):
		from django.template.defaultfilters import slugify
		if not self.pk:
		   self.created = timezone.now()
		else:
			if not self.created:
				self.created = timezone.now()
			self.modified = timezone.now()
		self.slug = orig = slugify(self.__str__())
		for x in itertools.count(1):
			if not Case.objects.filter(slug=self.slug).exists():
				break
			self.slug = '%s-%d' % (orig, x)
		models.Model.save(self,force_insert,force_update)


## Linked Models
class CaseEntity(ObjectDescription):
	""" Abstract model to contain information about a case entity.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		role (str, optional) [500] : Role in Case
		type (ENTITY_TYPE_CHOICES) [2]: Entity Type
		description (str, optional) [1000] : Description
		created (date, auto) : Date Created
		modified (date,auto) : Date Modified
		created_by (User, auto) : Created by
		modified_by (User, auto) : Modified by     

	"""

	# General Fields
	role = models.CharField(
		max_length=500, 
		blank=True, 
		null=True,  
		verbose_name=_("Role"),
		help_text=_("(Optional) Role of Entity"))

	type = models.CharField(
		max_length=3, 
		choices=ENTITY_TYPE_CHOICES, 
		verbose_name=_("Type"),
		help_text=_("(Optional) Type of Entity"))

	# Linked Fields

	# Auto Fields

	class Meta:
		abstract = True


class CasePerson(CaseEntity):
	""" Model to contain information about a case person.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		person (Person) : Case Person
		case (Case) : Case
		role (str, optional) [500] : Role in Case
		type (ENTITY_TYPE_CHOICES) [2]: Entity Type
		description (str, optional) [1000] : Description
		created (date, auto) : Date Created
		modified (date,auto) : Date Modified
		created_by (User, auto) : Created by
		modified_by (User, auto) : Modified by

	Methods:
		edit_url (URL) : Gets Case Person edit url
		case_url (URL) : Gets Case detail url

	"""

	# General Fields

	# Linked Fields
	person = models.ForeignKey(
		Person, 
		on_delete=models.DO_NOTHING, 
		blank=False,
		null=False,
		related_name=_('case_person_person'),
		verbose_name=_("Person"),
		help_text=_("Select Person"))

	case = models.ForeignKey(
		Case, 
		on_delete=models.DO_NOTHING, 
		blank=False,
		null=False, 
		related_name=_('case_person_case'),
		verbose_name=_("Case"),
		help_text=_("Select Case"))


	# Auto Fields

	history = HistoricalRecords()

	class Meta:
		verbose_name = _('Case Person')
		verbose_name_plural = _('Case Persons')

	def edit_url(self):
		""" Returns a url to edit the evidence
		
		Returns:
			caseevidence_edit

		"""
		return reverse('caseperson_edit', args=(self.case.pk, self.pk))

	def case_url(self):
		""" Returns a url for the case
		
		Returns:
			case_detail

		"""
		return reverse('case_detail', args=(self.case.pk,))

	def get_absolute_url(self):
		""" Returns a url for the person
		
		Returns:
			caseperson_detail
			
		"""
		return reverse('caseperson_detail', kwargs={'pk': self.pk})

	def __str__(self):
		""" Returns a human friendly string
		
		Returns:
			<Person First Name> <Person Middle Names> <Person Last Name>

		"""
		return '%s %s %s' % (
			_(self.person.first_name),
			_(self.person.middle_name), 
			_(self.person.last_name))


class CaseCompany(CaseEntity):
	"""  Model to contain information about a case company.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		company (Company) : Case Company
		case (Case) : Case
		role (str, optional) [500] : Role in Case
		type (ENTITY_TYPE_CHOICES) [2]: Entity Type
		description (str, optional) [1000] : Description
		created (date, auto) : Date Created
		modified (date,auto) : Date Modified
		created_by (User, auto) : Created by
		modified_by (User, auto) : Modified by

	Methods:
		edit_url (URL) : Gets Case Company edit url
		case_url (URL) : Gets Case detail url

	"""

	# General Fields

	# Linked Fields
	company = models.ForeignKey(
		Company, 
		on_delete=models.DO_NOTHING, 
		blank=False,
		null=False,
		related_name=_('case_company_company'),
		verbose_name=_("Company"),
		help_text=_("Select Company"))

	case = models.ForeignKey(
		Case, 
		on_delete=models.DO_NOTHING, 
		blank=False, 
		null=False, 
		related_name=_('case_company_case'),
		verbose_name=_("Case"),
		help_text=_("(Optional) Select Case"))
	
	# Auto Fields

	history = HistoricalRecords()
	
	class Meta:
		verbose_name = _('Case Company')
		verbose_name_plural = _('Case Companies')

	def edit_url(self):
		""" Returns a url to edit the evidence
		
		Returns:
			caseevidence_edit

		"""
		return reverse('casecompany_edit', args=(self.case.pk, self.pk))

	def case_url(self):
		""" Returns a url for the case
		
		Returns:
			case_detail

		"""
		return reverse('case_detail', args=(self.case.pk,))

	def get_absolute_url(self):
		""" Returns a url for the company
		
		Returns:
			casecompany_detail
			
		"""
		return reverse('casecompany_detail', kwargs={'pk': self.pk})

	def __str__(self):
		""" Returns a human friendly string
		
		Returns:
			Company Title

		"""
		return '%s' % _(self.company.title)


class CaseInventory(ObjectDescription):
	"""  Model to contain information about a case inventory item.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		active (Boolean, optional) : Case Device Active 
		device (Device) : Device
		case (Case) : Case
		description (str, optional) [1000]: Description
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified by

	Methods:
		edit_url (URL) : Gets Case Device edit url
		case_url (URL) : Gets Case detail url
		device_url (URL) : Gets Device detail url

	"""

	# General Fields
	active = models.BooleanField(
		default=True, 
		verbose_name=_("Active"),
		help_text=_("Is the case device Active"))

	# Linked Fields
	device = models.ForeignKey(
		Device, 
		on_delete=models.DO_NOTHING, 
		blank=False,
		null=False,
		related_name=_('case_inventory_device'),
		verbose_name=_("Device"),
		help_text=_("Select a Device"))

	case = models.ForeignKey(
		Case, 
		on_delete=models.CASCADE, 
		blank=False, 
		null=False,
		related_name=_('case_inventory_case'),
		verbose_name=_("Case"),
		help_text=_("Select a Case"))

	note = models.ManyToManyField(
		Note, 
		related_name=_('case_inventory_note'),
		verbose_name=_("Case Inventory Note"),
		help_text=_("Enter a case inventory Note"))

	# Auto Fields

	history = HistoricalRecords()
	
	class Meta:
		verbose_name = _('Case Device')
		verbose_name_plural = _('Case Devices')

	def edit_url(self):
		""" Returns a url to edit the evidence
		
		Returns:
			caseevidence_edit

		"""
		return reverse('casedevice_edit', args=(self.case.pk, self.pk))

	def case_url(self):
		""" Returns a url for the case
		
		Returns:
			case_detail

		"""
		return reverse('case_detail', args=(self.case.pk,))

	def device_url(self):
		""" Returns a url for the device
		
		Returns:
			device_detail

		"""
		return reverse('device_detail', args=(self.device.pk,))

	def get_absolute_url(self):
		""" Returns a url for the device
		
		Returns:
			casedevice_detail
			
		"""
		return reverse('casedevice_detail', kwargs={'pk': self.pk})

	def save(self,force_insert=False, force_update=False):
		models.Model.save(self,force_insert,force_update)


class CaseEvidence(Evidence):
	""" Model to contain information about case evidence.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		case (Case) : Case
		title (str) [128]: Evidence title
		reference (str, optional) [50]: Reference code
		bag_number (str, optional) [50]: Bag number
		location (str, optional) [250]: Location of the evidence
		File_location (file, optional): Location for evidence file
		image_upload (file, optional): Location for the evidence image
		qr_code (str, optional) [128]: QR Code 
		retention_reminder_sent (boolean, optional): Retention reminder sent
		retention_start_date (date, optional): Retention start date
		retention_end_date (date, optional): Retention end date
		chain_of_custody (ChainOfCustody, optional): Chain of custody
		type (EvidenceType, optional): Type of Evidence
		status (EvidenceStatus, optional): Status of the Evidence
		priority (EvidencePriority, optional): Priority of the Evidence
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

	Methods:
		edit_url (URL) : Gets Evidence edit url
		case_url (URL) : Gets Case detail url
	
	"""

	## General Fields ##

	## Linked Fields ##
	case = models.ForeignKey(
		Case, 
		on_delete=models.DO_NOTHING, 
		verbose_name=_("Case"),
		help_text=_("Select Case"))

	# Auto Fields

	history = HistoricalRecords()
	
	class Meta:
		verbose_name = _('Case Evidence')
		verbose_name_plural = _('Case Evidence')

	def edit_url(self):
		""" Returns a url to edit the evidence
		
		Returns:
			caseevidence_edit

		"""
		return reverse('caseevidence_edit', args=(self.case.pk, self.pk))

	def case_url(self):
		""" Returns a url for the case
		
		Returns:
			case_detail

		"""
		return reverse('case_detail', args=(self.case.pk,))

	def get_absolute_url(self):
		""" Returns a url for the evidence
		
		Returns:
			caseevidence_detail
			
		"""
		return reverse('caseevidence_detail', kwargs={'pk': self.pk})

	def save(self,force_insert=False, force_update=False):
		from django.template.defaultfilters import slugify
		if not self.pk:
		   self.created = timezone.now()
		else:
			if not self.created:
				self.created = timezone.now()
			self.modified = timezone.now()
		self.slug = orig = slugify(self.__str__())
		for x in itertools.count(1):
			if not CaseEvidence.objects.filter(slug=self.slug).exists():
				break
			self.slug = '%s-%d' % (orig, x)
		models.Model.save(self,force_insert,force_update)


class CaseEvent(Event):
	"""  Model to contain information about a case event.

	Args:
		history (HistoricalRecord, auto) : Historical records of object
		case (Case) : Case
		company (Company, optional) : Company
		person (Person, optional) : Person
		evidence (Evidence, optional) : Evidence
		title (str) [128]: Title for the Task 
		image_upload (file, optional): Location for a task image
		description (str, optional) [1000]: Description
		date (date, optional): Date for the Task
		status (TaskStatus, optional): Status of the Task
		priority (TaskPriority, optional): Priority of the Task
		authorisation (Authorisation, optional): Authorisation of the Task
		manager (AUTH_USER_MODEL, optional): Task manager
		assigned_by (AUTH_USER_MODEL, optional): Assigned To
		assigned_to (AUTH_USER_MODEL, optional): Assigned By
		note (Note, optional): Notes relating to the Task
		private (bool, optional): Is private
		created (date, auto) : Date Created
		modified (date,auto) : Date Modified
		created_by (User, auto) : Created by
		modified_by (User, auto) : Modified by
		 
	Methods:
		edit_url (URL) : Gets Event edit url
		case_url (URL) : Gets Case detail url
		company_url (URL) : Gets Company detail url
		person_url (URL) : Gets Person detail url

	"""

	# General Fields

	# Linked Fields 
	case = models.ForeignKey(
		Case, 
		on_delete=models.CASCADE, 
		blank=False, 
		null=False,
		related_name=_('case_event_case'),
		verbose_name=_("Case"),
		help_text=_("Select a Case"))
	
	person = models.ManyToManyField(
		Person, 
		related_name=_('case_event_person'),
		verbose_name=_("Persons"),
		help_text=_("Select Persons"))

	company = models.ManyToManyField(
		Company, 
		related_name=_('case_event_company'),
		verbose_name=_("Companies Involved"),
		help_text=_("Select Companies"))

	evidence = models.ManyToManyField(
		CaseEvidence, 
		related_name=_('case_event_evidence'),
		verbose_name=_("Evidence Involved"),
		help_text=_("Select Evidence"))

	# Auto Fields
	
	history = HistoricalRecords()

	class Meta:
		verbose_name = _('Case Event')
		verbose_name_plural = _('Case Event')

	def edit_url(self):
		""" Returns a url to edit the evidence
		
		Returns:
			caseevidence_edit

		"""
		return reverse('caseevent_edit', args=(self.case.pk, self.pk))

	def case_url(self):
		""" Returns a url for the case
		
		Returns:
			case_detail

		"""
		return reverse('case_detail', args=(self.case.pk,))

	def company_url(self):
		""" Returns a url for the company
		
		Returns:
			company_detail

		"""
		return reverse('company_detail', args=(self.company.pk,))
	
	def person_url(self):
		""" Returns a url for the person
		
		Returns:
			person_detail

		"""
		return reverse('person_detail', args=(self.person.pk,))

	def get_absolute_url(self):
		""" Returns a url for the event
		
		Returns:
			caseevent_detail
			
		"""
		return reverse('caseevent_detail', kwargs={'pk': self.pk})
	
	def save(self,force_insert=False, force_update=False):
		from django.template.defaultfilters import slugify
		if not self.pk:
		   self.created = timezone.now()
		else:
			if not self.created:
				self.created = timezone.now()
			self.modified = timezone.now()
		self.slug = orig = slugify(self.__str__())
		for x in itertools.count(1):
			if not CaseEvent.objects.filter(slug=self.slug).exists():
				break
			self.slug = '%s-%d' % (orig, x)
		models.Model.save(self,force_insert,force_update)


class CaseTask(Task):
	""" Linked model to contain information about a case task.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		case (Case) : Case
		event (Event, optional) : Case Events
		device (Devices, optional) : Case Devices
		evidence (Evidence, optional) : Case Evidence
		note (Note, optional) : Task Notes
		person (Person, optional) : Case Persons
		company (Company, optional) : Case Companies
		title (str) [128]: Title for the Task 
		location (str, optional) [250]: Location for the task
		description (str, optional) [1000]: Description
		deadline (date, optional): Deadline for the Task
		category (TaskCategory, optional): Category of Task
		status (TaskStatus, optional): Status of the Task
		priority (TaskPriority, optional): Priority of the Task
		authorisation (Authorisation, optional): Authorisation of the Task
		manager (AUTH_USER_MODEL, optional): Task manager
		assigned_by (AUTH_USER_MODEL, optional): Assigned To
		assigned_to (AUTH_USER_MODEL, optional): Assigned By
		private (bool, optional): Is private
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified by

	Methods:
		edit_url (URL) : Gets Task edit url
		case_url (URL) : Gets Case detail url
		event_url (URL) : Gets CaseEvent detail url
		device_url (URL) : Gets Device detail url
		evidence_url (URL) : Gets CaseEvidence detail url
		person_url (URL) : Gets Case detail url
		company_url (URL) : Gets Case detail url

	"""

	# General Fields
	
	# Linked Fields
	case = models.ForeignKey(
		Case, 
		on_delete=models.CASCADE, 
		blank=False, 
		null=False,
		related_name=_('case_task_case'),
		verbose_name=_("Case"),
		help_text=_("Select a Case"))
	  
	event = models.ManyToManyField(
		CaseEvent, 
		related_name=_('case_task_event'),
		verbose_name=_("Events Involved"),
		help_text=_("Select Events"))
	
	device = models.ManyToManyField(
		CaseInventory, 
		related_name=_('case_task_device'), 
		verbose_name=_("Devices Involved"),
		help_text=_("Select Evidence"))
	
	evidence = models.ManyToManyField(
		CaseEvidence, 
		related_name=_('case_task_evidence'),
		verbose_name=_("Evidence Involved"),
		help_text=_("Select Evidence"))

	person = models.ManyToManyField(
		Person, 
		related_name=_('case_task_person'),
		verbose_name=_("Persons Involved"),
		help_text=_("Select Persons"))

	company = models.ManyToManyField(
		Company, 
		related_name=_('case_task_company'),
		verbose_name=_("Companies Involved"),
		help_text=_("Select Companies"))

	# Auto Fields

	history = HistoricalRecords()
	
	class Meta:
		verbose_name = _('Case Task')
		verbose_name_plural = _('Case Task')

	def edit_url(self):
		""" Returns a url to edit the evidence
		
		Returns:
			caseevidence_edit

		"""
		return reverse('casetask_edit', args=(self.case.pk, self.pk))

	def case_url(self):
		""" Returns a url for the case
		
		Returns:
			case_detail

		"""
		return reverse('case_detail', args=(self.case.pk,))
	
	def save(self,force_insert=False, force_update=False):
		from django.template.defaultfilters import slugify
		if not self.pk:
		   self.created = timezone.now()
		else:
			if not self.created:
				self.created = timezone.now()
			self.modified = timezone.now()
		self.slug = orig = slugify(self.__str__())
		for x in itertools.count(1):
			if not CaseTask.objects.filter(slug=self.slug).exists():
				break
			self.slug = '%s-%d' % (orig, x)
		models.Model.save(self,force_insert,force_update)

	#def event_url(self):
	#    """ Returns a url for the events
		
	#    Returns:
	#        event_detail

	#    """
	#    return reverse('caseevent_detail', args=(self.event.pk,))

	#def device_url(self):
	#    """ Returns a url for the device
		
	#    Returns:
	#        device_detail

	#    """
	#    return reverse('casedevice_detail', args=(self.device.pk,))

	#def evidence_url(self):
	#    """ Returns a url for the evidence
		
	#    Returns:
	#        evidence_detail

	#    """
	#    return reverse('caseevidence_detail', args=(self.evidence.pk,))

	#def person_url(self):
	#    """ Returns a url for the person
		
	#    Returns:
	#        person_detail

	#    """
	#    return reverse('person_detail', args=(self.person.pk,))

	#def company_url(self):
	#    """ Returns a url for the company
		
	#    Returns:
	#        company_detail

	#    """
	#    return reverse('company_detail', args=(self.company.pk,))

	def get_absolute_url(self):
		""" Returns a url for the task
		
		Returns:
			casetask_detail
			
		"""
		return reverse('casetask_detail', kwargs={'pk': self.pk})