# Entity Models #

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup

## Admin Models
class Country(models.Model):
    # General Fields
    code = models.CharField(max_length=4, primary_key=True)
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Country")
    lat = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Latitude")
    lng = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Longtitude")

    # Linked Fields
    # Auto Fields

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        
    def __str__(self):
        return '%s' % _(self.title)
  
    
class State(models.Model):
    # General Fields
    short_name = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Abbreviation")
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="State")

    # Linked Fields
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

    # Auto Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name="State"
        verbose_name_plural="States"
        unique_together = ("short_name","country")
        
    def __str__(self):
        return "%s, %s" % (self.title,self.country.code)


class Note(models.Model):
    # General Fields
    text = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Note")

    # Linked Fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='note_author', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Note Author")

    # Auto Fields
    added = models.DateTimeField(auto_now=False, null=True, verbose_name="Added")

    history = HistoricalRecords()

    class Meta:
        verbose_name="Note"
        verbose_name_plural="Notes"
        
    def __str__(self):
        return "%s" % self.text


class ContactMethod(models.Model):
    # General Fields
    location = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Location")
    primary = models.BooleanField(default=False)
    
    history = HistoricalRecords()

    # Linked Fields
    # Auto Fields

    class Meta:
        abstract = True
 
        
class Address(ContactMethod):
    # General Fields
    line1 = models.CharField(max_length=255, null=True, blank=True)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    line3 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    #state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    postcode = models.CharField(max_length=31, blank=True)
    type = models.PositiveSmallIntegerField(choices=[(1,'Physical'),(2,'Postal'),(3,'Other')])

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name="Address"
        verbose_name_plural="Addresses"
        
    def __unicode__(self):
        rv = self.line1
        if self.line2:
            rv += ', '+self.line2
        if self.line3:
            rv += ', '+self.line3
        rv += ', '+self.city
        rv += ', '+self.state.short_name
        if self.zip:
            rv += ', '+self.zip
        rv += ', '+self.state.country.code
        return rv

    def __str__(self):
        return self.__unicode__()
   
    
class Telephone(ContactMethod):
    # General Fields
    number = models.CharField(max_length=63, db_index=True)
    type = models.PositiveSmallIntegerField(choices=[(1,'Fixed'),(2,'Mobile'),(3,'Fax')])

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.number
   
    
class Email(ContactMethod):
    # General Fields
    email = models.EmailField()

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.email

    def url(self):
        return "mailto:%s" % self.email
    

class Website(ContactMethod):
    # General Fields
    url = models.URLField()

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.url


class Social(ContactMethod):
    # General Fields
    service = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Social Media Service")
    alias = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Social Media Alias")
    url = models.URLField()

    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.url


class Prefix(models.Model):    
    # General Fields
    title = models.CharField(max_length=55, blank=True)
    
    # Linked Fields
    # Auto Fields
    
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.title