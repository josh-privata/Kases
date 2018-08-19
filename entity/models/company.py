# Company Models #

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup
from entity.models.entity import Address, Telephone, Email, Website, Social, Prefix, ContactMethod
from django.utils.timezone import now as timezone_now

## Admin Models
class CompanyAuthorisation(Authorisation):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Company Authorisation')
        verbose_name_plural = _('Company Authorisations')

    #def get_absolute_url(self):
    #    return reverse('company_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title
    

class CompanyClassification(Classification):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Company Classification')
        verbose_name_plural = _('Company Classifications')

    #def get_absolute_url(self):
    #    return reverse('company_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CompanyType(Type):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Company Type')
        verbose_name_plural = _('Company Types')

    #def get_absolute_url(self):
    #    return reverse('company_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CompanyCategory(Category):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Company Category')
        verbose_name_plural = _('Company Categories')

    #def get_absolute_url(self):
    #    return reverse('company_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CompanyStatus(Status):
    # General Fields
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Company Status')
        verbose_name_plural = _('Company Status')

    #def get_absolute_url(self):
    #    return reverse('company_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class CompanyStatusGroup(StatusGroup):
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
    status = models.ManyToManyField(CompanyStatus, blank=True, verbose_name="Company Status")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Company Status Group')
        verbose_name_plural = _('Company Status Groups')

    #def get_absolute_url(self):
    #    return reverse('company_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title

    
class CompanyAddress(ContactMethod):
    # General Fields
    line1 = models.CharField(max_length=255, null=True, blank=True)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    line3 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    #state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    postcode = models.CharField(max_length=31, blank=True)

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


## Main Models
class Company(models.Model):
    # General Fields
    title = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="Company Title")
    code = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="Issuer Code")
    #image = models.ImageField(upload_to='mugshots',null=True, blank=True)
    notes = models.TextField(max_length=255, null=True, blank=True, verbose_name="Company Notes")
    primary_market = models.TextField(max_length=255, null=True, blank=True, verbose_name="Primary Market")
    industry = models.TextField(max_length=255, null=True, blank=True, verbose_name="Industry")
    
    # Linked Fields
    prefix = models.ForeignKey(Prefix, on_delete=models.DO_NOTHING, null=True, blank=True)
    #social = models.ManyToManyField(Social, verbose_name="Social")
    address = models.ManyToManyField(CompanyAddress, verbose_name="Address")
    telephone = models.ManyToManyField(Telephone, verbose_name="Telephone")
    email = models.ManyToManyField(Email, verbose_name="Email")
    website = models.ManyToManyField(Website, verbose_name="Website")
    type = models.ForeignKey(CompanyType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Company Type")
    category = models.ForeignKey(CompanyCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Company Category")
    status = models.ForeignKey(CompanyStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Company Status")
    classification = models.ForeignKey(CompanyClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Company Classification")
    authorisation = models.ForeignKey(CompanyAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Company Authorisation")
    
    # Auto Fields
    slug = models.SlugField(editable=False, null=True, blank=True)
    created = models.DateTimeField(_("Creation date and time"),editable=False,)
    modified = models.DateTimeField(_("Modification date and time"),null=True,editable=False,)

    class Meta:
        verbose_name_plural = _("People")
        
    def __str__(self):
        return "%s" % (self.title)
    
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
        if not (self.pk):
            self.save(force_update=True)
        return reverse('company_detail',args=[self.pk])

    def save(self,force_insert=False, force_update=False):
        from django.template.defaultfilters import slugify
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.pk:
           self.created = timezone_now()
        else:
            if not self.created:
                self.created = timezone_now()
            self.modified = timezone_now()
        models.Model.save(self,force_insert,force_update)   