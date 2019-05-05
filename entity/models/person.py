# Person Models #

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from utils.choices import PREFIX
from utils.choices import GENDER
from utils.models import ObjectDescription
from utils.models import Authorisation
from utils.models import BaseObject
from entity.models.entity import Address
from entity.models.entity import  Telephone
from entity.models.entity import Email
from entity.models.entity import Website
from entity.models.entity import Social
from entity.models.entity import ContactMethod
from entity.models.company import Company


## Admin Models
class PersonClassification(BaseObject):
    """ Model to contain information about person classification.

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
        verbose_name = _('Person Classification')
        verbose_name_plural = _('Person Classifications')


class PersonType(BaseObject):
    """ Model to contain information about person type.

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
        verbose_name = _('Person Type')
        verbose_name_plural = _('Person Types')


class PersonCategory(BaseObject):
    """ Model to contain information about person category.

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
        verbose_name = _('Person Category')
        verbose_name_plural = _('Person Categories')


class PersonStatus(BaseObject):
    """ Model to contain information about person status.

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
        verbose_name = _('Person Status')
        verbose_name_plural = _('Person Status')


class PersonStatusGroup(BaseObject):
    """ Model to contain information about person status groups.

    Args:
        status (PersonStatus): Status in group
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
        PersonStatus, 
        blank=True, 
        verbose_name=_("Person Status"),
        help_text=_("Select Person Status"))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Person Status Group')
        verbose_name_plural = _('Person Status Groups')


class Employment(models.Model):
    """ Model to contain information about person's employment.

    Args:
        job_title (str, optional) [125]: Job Title
        notes (str, optional) [200]: Notes
        date_start (Date, optional) : Start Date
        date_finish (Date, optional) : Finish Date
        salary (int, optional) : Salary
        current (boolean, optional) : Current
        company (Company, optional) : Company

    """

    ## General Fields ##
    job_title = models.CharField(
        max_length=125, 
        null=True, 
        blank=True, 
        verbose_name=_("Job Title"),
        help_text=_("Enter the job title"))
    
    notes = models.CharField(
        max_length=200, 
        null=True, 
        blank=True, 
        verbose_name=_("Notes"),
        help_text=_("Enter notes"))

    date_start = models.DateTimeField(
        auto_now=False, 
        blank=True, 
        null=True, 
        verbose_name=_("Date Started"),
        help_text=_("Enter the start date"))

    date_finish = models.DateTimeField(
        auto_now=False, 
        blank=True, 
        null=True, 
        verbose_name=_("Date Finished"),
        help_text=_("Enter the finish date"))

    salary = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name=_("Salary"),
        help_text=_("Enter the salary"))

    current = models.BooleanField(
        default=False, 
        blank=True, 
        verbose_name=_("Current"),
        help_text=_("(Optional) Is Current"))

    company = models.ForeignKey(
        Company, 
        on_delete=models.DO_NOTHING, 
        null=True, 
        blank=True, 
        related_name=_('person_company'),
        verbose_name=_("Company"),
        help_text=_("Select the company"))


    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Employment')
        verbose_name_plural = _('Employment')


## Main Models
class Person(ObjectDescription):
    """ Model to contain information about a person.

    Args:
        history (HistoricalRecord, auto): Historical records of object
        prefix (int, optional) : Prefix
        first_name (str, optional) [125]: First Name
        middle_names (str, optional) [125]: Middle Names
        last_name (str, optional) [125]: Last Name
        suffix (str, optional) [55]: Suffix
        nickname (str, optional) [200]: Nicknames
        aliases (str, optional) [200]: Aliases
        gender (int, optional) : Gender
        dob (Date, optional) : Date of Birth
        height (int, optional) : Height in cm 
        weight (int, optional) : Weight in kg
        age (int, optional) : Age
        spouse (Person, optional) : Spouse
        image_upload (file, optional): Location for the evidence image
        taxfile (str, optional) [35] : Taxfile Number 
        address (Address, optional) : Address
        telephone (Telephone, optional) : Telephone
        email (Email, optional) : Email
        website (website, optional) : Website
        social (Social, optional) : Social media
        type (PersonType, optional) : Person Type
        status (PersonStatus, optional) : Person  Status
        classification (PersonClassification, optional) : Person Calssification
        category (PersonCategory, optional) : Person Category
        authorisation (Authorisation, optional) : Person Authorisation
        employment (Employment, optional): Employment History
        affiliations (Groups, optional): Affiliations
        private (bool, optional): Is private
        description (str, optional) [1000]: Description
        created (date, auto): Date Created
        modified (date,auto): Date Modified
        created_by (User, auto): Created by
        modified_by (User, auto): Modified by
        slug (slug, optional) : Slug of name

    Methods:
        primary_address (Address) : Gets Primary Address
        primary_telephone (Telephone) : Gets Primary Telephone
        primary_email (Email) : Gets Primary Email
        primary_website (Email) : Gets Primary Website
        primary_social (Email) : Gets Primary Social Account
        current_employment (Employment) : Gets Current Employment
        previous_employment (Employment) : Gets Previous Employment
    
    """

    ## Name Fields ##
    prefix = models.PositiveIntegerField(
        choices=PREFIX, 
        null=True, 
        blank=True,
        default='1',
        verbose_name=_("Prefix"),
        help_text=_("Select prefix"))

    first_name = models.CharField(
        max_length=125, 
        null=True, 
        blank=True, 
        verbose_name=_("First Name"),
        help_text=_("Enter a first name"))

    middle_names = models.CharField(
        max_length=125, 
        null=True, 
        blank=True, 
        verbose_name=_("Middle Names"),
        help_text=_("Enter middle names"))

    last_name = models.CharField(
        max_length=125, 
        null=True, 
        blank=True, 
        verbose_name=_("Last Name"),
        help_text=_("Enter a last name"))

    suffix = models.CharField(
        max_length=55, 
        null=True, 
        blank=True, 
        verbose_name=_("Suffix"),
        help_text=_("Enter a suffix"))
    
    nickname = models.CharField(
        max_length=200, 
        null=True, 
        blank=True, 
        verbose_name=_("Nickname"),
        help_text=_("Enter any nicknames"))

    aliases = models.CharField(
        max_length=200, 
        null=True, 
        blank=True, 
        verbose_name=_("Aliases"),
        help_text=_("Enter any known aliases"))

    ## Personal Fields ##
    gender = models.PositiveIntegerField(
        choices=GENDER, 
        null=True, 
        blank=True, 
        verbose_name=_("Gender"),
        help_text=_("Select the gender"))

    dob = models.DateTimeField(
        auto_now=False, 
        blank=True, 
        null=True, 
        verbose_name=_("Date Of Birth"),
        help_text=_("Select the date of birth"))

    height = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name=_("Height"),
        help_text=_("Enter the person's height in centimeters"))

    weight = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name=_("Weight"),
        help_text=_("Enter the person's weight in kilograms"))

    age = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name=_("Age"),
        help_text=_("Enter the person's age"))

    #spouse = models.ForeignKey(
    #    Person, 
    #    on_delete=models.DO_NOTHING, 
    #    null=True, 
    #    blank=True,
    #    related_name=_('person_spouse'), 
    #    verbose_name=_("Spouse"),
    #    help_text=_("Select the spouse"))
    
    image_upload = models.FileField(
        upload_to='',
        blank=True, 
        null=True, 
        verbose_name=_("Image"),
        help_text=_("Upload an image for the Person"))

    taxfile = models.CharField(
        max_length=35, 
        null=True, 
        blank=True, 
        verbose_name=_("Tax File Number"),
        help_text=_("Enter the tax file number"))

    ## Contact Fields ##
    address = models.ManyToManyField(
        Address,
        related_name=_('person_address'),
        verbose_name=_("Address"),
        help_text=_("Enter the address"))

    telephone = models.ManyToManyField(
        Telephone,
        related_name=_('person_telephone'),
        verbose_name=_("Telephone"),
        help_text=_("Enter the telephone number"))

    email = models.ManyToManyField(
        Email,
        related_name=_('person_email'),
        verbose_name=_("Email"),
        help_text=_("Enter the email address"))

    website = models.ManyToManyField(
        Website,
        related_name=_('person_website'),
        verbose_name=_("Website"),
        help_text=_("Enter the website"))

    social = models.ManyToManyField(
        Social,
        related_name=_('person_social'),
        verbose_name=_("Social"),
        help_text=_("Enter the social media service"))

    ## Linked Fields ##
    type = models.ForeignKey(
        PersonType, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('person_type'),
        verbose_name=_("Person Type"),
        help_text=_("Select the type"))

    status = models.ForeignKey(
        PersonStatus, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('person_status'),
        verbose_name=_("Person Status"),
        help_text=_("Select the status"))

    classification = models.ForeignKey(
        PersonClassification, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('person_classification'),
        verbose_name=_("Person Classification"),
        help_text=_("Select the classification"))

    category = models.ForeignKey(
        PersonCategory, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('person_category'),
        verbose_name=_("Person Category"),
        help_text=_("Select the category"))

    authorisation = models.ForeignKey(
        Authorisation, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name=_('person_authorisation'),
        verbose_name=_("Person Authorisation"),
        help_text=_("Select the authorisation level"))
    
    employment = models.ManyToManyField(
        Employment,
        related_name=_('person_employment'),
        verbose_name=_("Employment"),
        help_text=_("Enter employment"))

    #affiliation = models.ManyToManyField(
    #    Group,
    #    related_name=_('person_affiliation'),
    #    verbose_name="Affiliation"),
    #    help_text=_("Select any affiliations"))

    ## Auto Fields ##
    slug = models.SlugField(
        editable=False, 
        null=True, 
        blank=True, 
        verbose_name=_("Name Slug"),
        help_text=_("Enter the slug"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")
        
    def __str__(self):
        return "%s, %s, %s" % (
            _(self.first_name),
            _(self.middle_names),
            _(self.last_name))
    
    def primary_address(self):
        try:
            return self.address.filter(primary=True)[0]
        except IndexError:
            if self.address.exists():
                return self.address.all()[0]
        return None

    def primary_telephone(self):
        try:
            return self.telephone.filter(primary=True)[0]
        except IndexError:
            if self.telephone.exists():
                return self.telephone.all()[0]
        return None
        
    def primary_email(self):
        try:
            return self.email.filter(primary=True)[0]
        except IndexError:
            if self.email.exists():
                return self.email.all()[0]
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

    def current_employment(self):
        try:
            employment = self.employment.filter(current=True)[0]
        except IndexError:
            employment = None
        return employment

    def previous_employment(self):
        try:
            employment = self.employment.filter(current=False)
        except IndexError:
            employment = None
        return employment
        
    def get_absolute_url(self):
        return reverse('person_detail',args=[self.pk])
    
    def save(self,force_insert=False, force_update=False):
        from django.template.defaultfilters import slugify
        if not self.pk:
           self.created = timezone.now()
        else:
            if not self.created:
                self.created = timezone.now()
            self.modified = timezone.now()
        self.slug = slugify(self.__str__())
        models.Model.save(self,force_insert,force_update)
