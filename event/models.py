## Event Models ##

## python imports
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from utils.models import ObjectDescription
from utils.models import Authorisation
from utils.models import Priority
from utils.models import BaseObject
from utils.models import Note
#import event.managers as managers


## Admin Models
class EventClassification(BaseObject):
	""" Model to contain information about an event classification.

	Args:
		history (HistoricalRecord, auto): Historical records of object
		title (str) [50]: Title
		colour (str, optional) [7]: Hexidecimal colour representation
		description (str, optional) [1000]: Description
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified byl 
	
	"""
	
	history = HistoricalRecords()

	class Meta:
		verbose_name = _('Event Classification')
		verbose_name_plural = _('Event Classifications')


class EventPriority(Priority):
	"""  Model to contain information about an event priority.

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
		verbose_name = _('Event Priority')
		verbose_name_plural = _('Event Priorities')


class EventCategory(BaseObject):
	""" Model to contain information about an event category.

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
		verbose_name = _('Event Category')
		verbose_name_plural = _('Event Categories')


class EventStatus(BaseObject):
	"""  Model to contain information about an event status.

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
		verbose_name = _('Event Status')
		verbose_name_plural = _('Event Status')


class EventStatusGroup(BaseObject):
	""" Model to contain information about a person status group.

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
		EventStatus, 
		blank=True, 
		verbose_name=_("Event Status"),
		help_text=_("Select Event Status"))
	
	history = HistoricalRecords()

	class Meta:
		verbose_name = _('Event Status Group')
		verbose_name_plural = _('Event Status Groups')


## Main Models
class Event(ObjectDescription):
	""" Abstract model to contain information about an event.

	Args:
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
		created (date, auto): Date Created
		modified (date,auto): Date Modified
		created_by (User, auto): Created by
		modified_by (User, auto): Modified by 
		slug (slug, Auto): Slug of title

	"""

	## General Fields ##
	title = models.CharField(
		max_length=128,
		blank=False,
		null=False,
		default=None,
		verbose_name=_("Title"),
		help_text=_("Enter a title for the Task"))

	image_upload = models.FileField(
		upload_to='',
		blank=True, 
		null=True, 
		verbose_name=_("Event Image"),
		help_text=_("Upload an image for the Task"))
	
	date = models.DateTimeField(
	   auto_now=False, 
	   null=False,
	   default=timezone.now(), 
	   verbose_name=_("Date"),
	   help_text=_("Select a date for the Task"))

	## Linked Fields ##
	classification = models.ForeignKey(
		EventClassification, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True, 
		verbose_name=_("Event Classification"),
		help_text=_("(Optional) Select the classification of Event"))

	category = models.ForeignKey(
		EventCategory, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True, 
		verbose_name=_("Event Category"),
		help_text=_("(Optional) Select the category of Event"))

	status = models.ForeignKey(
		EventStatus, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		verbose_name=_("Status"),
		help_text=_("(Optional) Select the status of the Event"))

	priority = models.ForeignKey(
		EventPriority, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		verbose_name=_("Priority"),
		help_text=_("(Optional) Select the priority of the Event"))

	authorisation = models.ForeignKey(
		Authorisation, 
		on_delete=models.SET_NULL, 
		blank=True, 
		null=True,
		verbose_name=_("Authorisation"),
		help_text=_("(Optional) Select the authorisation of the Event"))

	manager = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		blank=True, 
		null=True,
		related_name='Event_manager', 
		verbose_name=_("Event Manager"),
		help_text=_("(Optional) Select the Event Manager"))

	assigned_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		blank=True, 
		null=True,
		related_name='Event_assigned_by', 
		verbose_name=_("Assigned By"),
		help_text=_("(Optional) Select Event assigned by"))

	assigned_to = models.ManyToManyField(
		settings.AUTH_USER_MODEL, 
		blank=True,
		related_name='Event_assigned_to', 
		verbose_name=_("Assigned To"),
		help_text=_("(Optional) Select Event assigned to"))

	note = models.ManyToManyField(
		Note, 
		blank=True, 
		related_name='event_note', 
		verbose_name=_("Note"),
		help_text=_("(Optional) Enter a note relating to the Event"))

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

