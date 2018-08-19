# Person Models #

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup
from entity.models.entity import Address, Telephone, Email, Website, Social, Prefix, ContactMethod
from entity.models.company import Company
from django.utils.timezone import now as timezone_now

## Admin Models
class PersonAuthorisation(Authorisation):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Person Authorisation')
        verbose_name_plural = _('Person Authorisations')

    #def get_absolute_url(self):
    #    return reverse('person_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    

class PersonClassification(Classification):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Person Classification')
        verbose_name_plural = _('Person Classifications')

    #def get_absolute_url(self):
    #    return reverse('person_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class PersonType(Type):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Person Type')
        verbose_name_plural = _('Person Types')

    #def get_absolute_url(self):
    #    return reverse('person_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class PersonCategory(Category):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Person Category')
        verbose_name_plural = _('Person Categories')

    #def get_absolute_url(self):
    #    return reverse('person_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class PersonStatus(Status):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Person Status')
        verbose_name_plural = _('Person Status')

    #def get_absolute_url(self):
    #    return reverse('person_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class PersonStatusGroup(StatusGroup):
    ## Choices
    # CREATED = 'Created'
    # PENDING = 'Awaiting Authorisation'
    # REJECTED = 'Rejected'
    # OPEN = 'Open'
    # Active = 'Active'
    # CLOSED = 'Closed'
    # ARCHIVED = 'Archived'
    ## Choice Groups
    # closedStatuses = [CLOSED, ARCHIVED]
    # all_statuses = [CREATED, OPEN, CLOSED, ARCHIVED, PENDING, REJECTED]
    # approved_statuses = [CREATED, OPEN, CLOSED, ARCHIVED]
    # active_statuses = [CREATED, PENDING, REJECTED, OPEN]
    # workable_statuses = [CREATED, OPEN]
    # forensic_statuses = [OPEN]
    
    # General Fields
    # Linked Fields
    status = models.ManyToManyField(PersonStatus, blank=True, verbose_name="Person Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Person Status Group')
        verbose_name_plural = _('Person Status Groups')

    #def get_absolute_url(self):
    #    return reverse('person_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


## Main Models
class Person(models.Model):
    # General Fields
    #image = models.ImageField(upload_to='mugshots',null=True, blank=True, verbose_name="Person Type")
    first_name = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="Last Name")
    middle_names = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="Middle Names")
    nickname = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="Nickname")
    aliases = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="Aliases")
    suffix = models.CharField(max_length=55, null=True, blank=True, verbose_name="Suffix")
    notes = models.TextField(max_length=255, null=True, blank=True, verbose_name="Notes")
    
    # Detail Fields
    
    # Personal Fields
    gender = models.CharField(max_length=55, null=True, blank=True, verbose_name="Gender")
    birthday = models.DateTimeField(auto_now=False, blank=True, null=True, verbose_name="Birthday")
    anniversary = models.DateTimeField(auto_now=False, blank=True, null=True, verbose_name="Anniversary")
    height = models.CharField(max_length=55, null=True, blank=True, verbose_name="Height")
    weight = models.CharField(max_length=55, null=True, blank=True, verbose_name="Weight")
    age = models.CharField(max_length=55, null=True, blank=True, verbose_name="Age")

    #spouse = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Spouse")

    # Work Fields
    taxfile = models.CharField(max_length=55, null=True, blank=True, verbose_name="Tax File Number")
    date_started = models.DateTimeField(auto_now=False, blank=True, null=True, verbose_name="Date Started")
    salary = models.CharField(max_length=55, null=True, blank=True, verbose_name="Salary")
    job_title = models.CharField(max_length=55, null=True, blank=True, verbose_name="Job Title")
    role = models.CharField(max_length=55, null=True, blank=True, verbose_name="Role")
    #company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Company")

    # Contact Fields Social
    #social = models.ManyToManyField(Social, verbose_name="Social")
    address = models.ManyToManyField(Address, verbose_name="Address")
    telephone = models.ManyToManyField(Telephone, verbose_name="Telephone")
    email = models.ManyToManyField(Email, verbose_name="Email")
    website = models.ManyToManyField(Website, verbose_name="Website")

    # Other Fields
    prefix = models.ForeignKey(Prefix, on_delete=models.DO_NOTHING, null=True, blank=True)
    type = models.ForeignKey(PersonType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Type")
    status = models.ForeignKey(PersonStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Status")
    classification = models.ForeignKey(PersonClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Classification")
    category = models.ForeignKey(PersonCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Category")
    authorisation = models.ForeignKey(PersonAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Authorisation")
    
    # Auto Fields
    slug_first = models.SlugField(editable=False, null=True, blank=True, verbose_name="First Name Slug")
    slug_last = models.SlugField(editable=False, null=True, blank=True, verbose_name="Last Name Slug")
    slug_middle = models.SlugField(editable=False, null=True, blank=True, verbose_name="Middle Name Slug")
    created = models.DateTimeField(_("Creation date and time"),editable=False,)
    modified = models.DateTimeField(_("Modification date and time"),null=True,editable=False,)

    class Meta:
        verbose_name_plural = _("People")
        
    def __str__(self):
        return "%s, %s" % (self.last_name,self.first_name)
    
    def primary_address(self):
        try:
            return self.addresses.filter(primary=True)[0]
        except IndexError:
            return None

    def primary_telephone(self):
        try:
            return self.telephones.filter(primary=True)[0]
        except IndexError:
            if self.telephones.exists():
                return self.telephones.all()[0]
            return None
        
    def primary_email(self):
        try:
            return self.emails.filter(primary=True)[0]
        except IndexError:
            return None
        
    def get_absolute_url(self):
        if not (self.slug_first or self.slug_last):
            self.save(force_update=True)
        return reverse('person_detail',args=[self.pk])
    
    def save(self,force_insert=False, force_update=False):
        from django.template.defaultfilters import slugify
        if not self.slug_last:
            self.slug_last = slugify(self.last_name)
        if not self.slug_first:
            self.slug_first = slugify(self.first_name)
        if not self.slug_middle:
            self.slug_middle = slugify(self.middle_names)
        if not self.pk:
           self.created = timezone_now()
        else:
            if not self.created:
                self.created = timezone_now()
            self.modified = timezone_now()
        models.Model.save(self,force_insert,force_update)