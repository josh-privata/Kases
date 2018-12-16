# Company Models #

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from utils.choices import INDUSTRY
from utils.models import ObjectDescription
from utils.models import Authorisation
from utils.models import BaseObject
from entity.models.entity import Address
from entity.models.entity import Telephone
from entity.models.entity import Email
from entity.models.entity import Website
from entity.models.entity import Social
from entity.models.entity import ContactMethod


## Admin Models
class CompanyClassification(BaseObject):
    """ Model to contain information about company classification.

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
        verbose_name = _('Company Classification')
        verbose_name_plural = _('Company Classifications')


class CompanyType(BaseObject):
    """ Model to contain information about company type.

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
        verbose_name = _('Company Type')
        verbose_name_plural = _('Company Types')


class CompanyCategory(BaseObject):
    """ Model to contain information about company category.

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
        verbose_name = _('Company Category')
        verbose_name_plural = _('Company Categories')


class CompanyStatus(BaseObject):
    """ Model to contain information about company status.

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
        verbose_name = _('Company Status')
        verbose_name_plural = _('Company Status')


class CompanyStatusGroup(BaseObject):
    """ Model to contain information about company status groups.

    Args:
        status (CompanyStatus): Status in group
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
        CompanyStatus, 
        blank=True, 
        verbose_name=_("Company Status"),
        help_text=_("Select Company Status"))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Company Status Group')
        verbose_name_plural = _('Company Status Groups')


## Main Models
class Company(ObjectDescription):
    """ Model to contain information about company.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        title (str, optional) [125]: Company Title
        code (str, optional) [5]: Stock Market Code
        logo_upload (FileField, optional) : Company logo upload
        industry (int, optional) : Industry
        address (Address, optional) : Address
        telephone (Telephone, optional) : Telephone
        email (Email, optional) : Email
        website (website, optional) : Website
        social (Social, optional) : Social media
        type (CompanyType, optional) : Company Type
        status (CompanyStatus, optional) : Company  Status
        classification (CompanyClassification, optional) : Company Calssification
        category (CompanyCategory, optional) : Company Category
        authorisation (Authorisation, optional) : Company Authorisation
        affiliations (Groups, optional): Affiliations
        private (bool, optional): Is private
        description (str, optional) [1000]: Description
        created (date, auto): Date Created
        modified (date,auto): Date Modified
        created_by (User, auto): Created by
        modified_by (User, auto): Modified by
        slug (slug, optional) : Title Slug
    
    Methods:
        primary_address (Address) : Gets Primary Address
        primary_telephone (Telephone) : Gets Primary Telephone
        primary_email (Email) : Gets Primary Email
        primary_website (Email) : Gets Primary Website
        primary_social (Email) : Gets Primary Social Account
    """

    ## General Fields ##
    title = models.CharField(
        max_length=125, 
        null=True, 
        blank=True, 
        verbose_name=_("Title"),
        help_text=_("Enter a title for the company"))

    code = models.CharField(
        max_length=5, 
        null=True, 
        blank=True, 
        verbose_name=_("Issuer Code"),
        help_text=_("Enter the issuer code for the company"))
    
    logo_upload = models.FileField(
        upload_to='',
        blank=True, 
        null=True, 
        verbose_name=_("Logo"),
        help_text=_("Upload an logo for the company"))

    industry = models.PositiveIntegerField(
        choices=INDUSTRY, 
        blank=True, 
        null=True, 
        verbose_name=_("Industry"),
        help_text=_("Select an industry for the company"))
    
    ## Contact Fields ##
    address = models.ManyToManyField(
        Address,
        related_name=_('company_address'),
        verbose_name=_("Address"),
        help_text=_("Enter the address"))

    telephone = models.ManyToManyField(
        Telephone,
        related_name=_('company_telephone'),
        verbose_name=_("Telephone"),
        help_text=_("Enter the telephone number"))

    email = models.ManyToManyField(
        Email,
        related_name=_('company_email'),
        verbose_name=_("Email"),
        help_text=_("Enter the email address"))

    website = models.ManyToManyField(
        Website,
        related_name=_('company_website'),
        verbose_name=_("Website"),
        help_text=_("Enter the website"))

    social = models.ManyToManyField(
        Social,
        related_name=_('company_social'),
        verbose_name=_("Social"),
        help_text=_("Enter the social media service"))

    ## Linked Fields ##
    type = models.ForeignKey(
        CompanyType, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('company_type'),
        verbose_name=_("Company Type"),
        help_text=_("Select the type"))

    status = models.ForeignKey(
        CompanyStatus, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('company_status'),
        verbose_name=_("Company Status"),
        help_text=_("Select the status"))

    classification = models.ForeignKey(
        CompanyClassification, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('company_classification'),
        verbose_name=_("Company Classification"),
        help_text=_("Select the classification"))

    category = models.ForeignKey(
        CompanyCategory, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('company_category'),
        verbose_name=_("Company Category"),
        help_text=_("Select the category"))

    authorisation = models.ForeignKey(
        Authorisation, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('company_authorisation'),
        verbose_name=_("Company Authorisation"),
        help_text=_("Select the authorisation level"))

    #affiliation = models.ManyToManyField(
    #    Group,
    #    related_name=_('company_affiliation'),
    #    verbose_name="Affiliation"),
    #    help_text=_("Select any affiliations")
    
    ## Auto Fields ##
    slug = models.SlugField(
        editable=False, 
        null=True, 
        blank=True, 
        verbose_name=_("Title Slug"),
        help_text=_("Enter the slug"))

    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = _("Companies")
        
    def __str__(self):
        return "%s" % (self.title)
    
    def primary_address(self):
        try:
            return self.addresses.filter(primary=True)[0]
        except IndexError:
            if self.telephones.exists():
                return self.telephones.all()[0]
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
            if self.telephones.exists():
                return self.telephones.all()[0]
        return None

    def primary_website(self):
        try:
            return self.website.filter(primary=True)[0]
        except IndexError:
            if self.website.exists():
                return self.website.all()[0]
        return None

    def primary_social(self):
        try:
            return self.social.filter(primary=True)[0]
        except IndexError:
            if self.social.exists():
                return self.social.all()[0]
        return None
        
    def get_absolute_url(self):
        if not (self.pk):
            self.save(force_update=True)
        return reverse('company_detail',args=[self.pk])

    def save(self,force_insert=False, force_update=False):
        from django.template.defaultfilters import slugify
        if not self.pk:
           self.created = timezone.now()
        else:
            if not self.created:
                self.created = timezone.now()
            self.modified = timezone.now()
        self.slug = slugify(self.title)
        models.Model.save(self,force_insert,force_update)   