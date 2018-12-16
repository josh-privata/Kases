# Entity Models #

from django.db import models
from django.urls import reverse
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _
from utils.choices import COUNTRIES
from utils.choices import PHONENUMBERTYPE
from utils.choices import ADDRESSTYPE


## Admin Models
class ContactMethod(models.Model):
    """ Abstract base class with common to all contact methods.

    Args:
        primary (boolean, optional) : Primary
        current (boolean, optional) : Current

    """

    # General Fields
    primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary"),
        help_text=_("Is primary"))

    current = models.BooleanField(
        default=True,
        verbose_name=_("Current"),
        help_text=_("Is current"))
    
    # Linked Fields
    # Auto Fields

    class Meta:
        abstract = True
 
        
class Address(ContactMethod):
    """ Model to contain information about an address.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        primary (boolean, optional) : Primary
        current (boolean, optional) : Current
        line1 (str, optional) [120]: Address Line 1
        line2 (str, optional) [120]: Address Line 2
        line3 (str, optional) [120]: Address Line 3
        city (str, optional) [100]: City
        state (str, optional) [75]: State
        country (str, optional) [3]: Country
        postcode (str, optional) [20]: Postcode
        type (int, optional) : Type
        location (str, optional) [125] : Location

    """

    # General Fields
    line1 = models.CharField(
        max_length=120, 
        null=True, 
        blank=True,
        verbose_name=_("Line 1"),
        help_text=_("Enter address line 1"))

    line2 = models.CharField(
        max_length=120, 
        null=True, 
        blank=True,
        verbose_name=_("Line 2"),
        help_text=_("Enter address line 2"))

    line3 = models.CharField(
        max_length=120, 
        null=True, 
        blank=True,
        verbose_name=_("Line 3"),
        help_text=_("Enter address line 3"))

    city = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name=_("City"),
        help_text=_("Enter the city"))

    state = models.CharField(
        max_length=75, 
        null=True, 
        blank=True,
        verbose_name=_("State"),
        help_text=_("Enter the state"))

    country = models.CharField(
        max_length=3, 
        choices=COUNTRIES, 
        blank=True, 
        null=True,
        verbose_name=_("Country"),
        help_text=_("Select the country"))

    postcode = models.CharField(
        max_length=20, 
        blank=True,
        null=True,
        verbose_name=_("Postcode"),
        help_text=_("Enter the postcode"))

    type = models.PositiveSmallIntegerField(
        choices=ADDRESSTYPE,
        verbose_name=_("Line 3"),
        help_text=_("Select the type of address"))

    location = models.CharField(
        max_length=125, 
        blank=True, 
        null=True, 
        default=None, 
        verbose_name=_("Location"),
        help_text=_("Enter the location"))

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name=_("Address")
        verbose_name_plural=_("Addresses")
        
    def __str__(self):
        """ Returns the full formatted address

        """

        if self.line1:
            address = self.line1
        if self.line2:
            address += ', ' + self.line2
        if self.line3:
            address += ', ' + self.line3
        if self.city:
            address += ', ' + self.city
        if self.state:
            address += ', ' + self.state
        if self.postcode:
            address += ', ' + self.postcode
        if self.country:
            address += ', ' + self.country
        return _(address)
   

class Email(ContactMethod):
    """ Model to contain information about an email address.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        primary (boolean, optional) : Primary
        current (boolean, optional) : Current
        email (EmailField, optional) : Email
        location (str, optional) [125] : Location
        
    Methods:
        url (URL) : Returns mailto: url

    """

    # General Fields
    email = models.EmailField(
        blank=True, 
        null=True, 
        default=None, 
        verbose_name=_("Email"),
        help_text=_("Enter email"))

    location = models.CharField(
        max_length=125, 
        blank=True, 
        null=True, 
        default=None, 
        verbose_name=_("Location"),
        help_text=_("Enter location"))

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % _(self.email)

    def url(self):
        return "mailto:%s" % _(self.email)


class Telephone(ContactMethod):
    """ Model to contain information about a telephone number.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        primary (boolean, optional) : Primary
        current (boolean, optional) : Current
        number (str, optional) [40] : Phone Number
        type (int, optional) : Type

    """

    # General Fields
    number = models.CharField(
        max_length=40, 
        blank=True, 
        null=True, 
        verbose_name=_("Phone Number"),
        help_text=_("Enter address line 1"))

    type = models.PositiveSmallIntegerField(
        choices=PHONENUMBERTYPE, 
        verbose_name=_("Type"),
        help_text=_("Enter address line 1"))

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % _(self.number)
     

class Website(ContactMethod):
    """ Model to contain information about a website.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        primary (boolean, optional) : Primary
        current (boolean, optional) : Current
        url (URLField) : URL

    """

    # General Fields
    url = models.URLField(
        verbose_name=_("Website URL"),
        help_text=_("Enter the website URL"))

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % _(self.url)


class Social(ContactMethod):
    """ Model to contain information about a social media service.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        primary (boolean, optional) : Primary
        current (boolean, optional) : Current
        service (str, optional) [125] : Service
        alias (str, optional) [125] : Online Alias
        url (URLField) : URL

    """

    # General Fields
    service = models.CharField(
        max_length=125, 
        blank=True, 
        null=True, 
        default=None, 
        verbose_name=_("Social Media Service"),
        help_text=_("Enter the social media service name"))

    alias = models.CharField(
        max_length=125, 
        blank=True, 
        null=True, 
        default=None, 
        verbose_name=_("Social Media Alias"),
        help_text=_("Enter the alias"))

    url = models.URLField(
        verbose_name=_("Profile URL"),
        help_text=_("Enter the profile URL"))

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % _(self.url)
