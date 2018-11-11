## User Models ##

## python imports
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords
from utils.models import ObjectDescriptionMixin, Authorisation, Category, Classification, Priority, Type, Status, StatusGroup
from entity.models.entity import Address, Telephone, Email, Website, Social, Prefix, ContactMethod



## Admin Models
class UserAuthorisation(Authorisation):
    """
    Inherited model to contain information about a User authorisation.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('User Authorisation')
        verbose_name_plural = _('User Authorisations')


class UserClassification(Classification):
    """
    Inherited model to contain information about a User classification.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('User Classification')
        verbose_name_plural = _('User Classifications')


class UserType(Type):
    """
    Inherited model to contain information about a User type.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('User Type')
        verbose_name_plural = _('User Types')


class UserPriority(Priority):
    """
    Inherited model to contain information about a User priority.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('User Priority')
        verbose_name_plural = _('User Priorities')


class UserCategory(Category):
    """
    Inherited model to contain information about a User category.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    
    """

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('User Category')
        verbose_name_plural = _('User Categories')


class UserStatus(Status):
    """
    Inherited model to contain information about a User status.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    
    """

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('User Status')
        verbose_name_plural = _('User Status')


class UserStatusGroup(StatusGroup):
    """
    Inherited model to contain information about a User status group.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    :status (optional): Status in group linked by Status model
    
    """

    # Linked Fields
    status = models.ManyToManyField(UserStatus, blank=True, verbose_name="User Status")

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('User Status Group')
        verbose_name_plural = _('User Status Groups')


## Main Models
class Profile(models.Model):
    """
    Model to contain information about a person.

    :first_name (optional):
    :last_name (optional):
    :middle_names (optional):
    :nickname (optional):
    :aliases (optional):
    :suffix (optional):
    :notes (optional):
    :image (optional):
    :gender (optional):
    :birthday (optional):
    :anniversary (optional):
    :height (optional):
    :weight (optional):
    :age (optional):
    :spouse (optional):
    :taxfile (optional):
    :date_started (optional):
    :salary (optional):
    :job_title (optional):
    :role (optional):
    :company (optional):
    :social (optional):
    :address (optional):
    :telephone (optional):
    :email (optional):
    :website (optional):
    :prefix (optional):
    :type (optional):
    :status (optional):
    :classification (optional):
    :category (optional):
    :authorisation (optional):
    :slug_first (optional):
    :slug_last (optional):
    :slug_middle (optional):
    :created (optional):
    :modified (optional):
    :description (optional): Description
    :private (optional): Is it private Boolean
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 

    """

    # General Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    bio = models.TextField(max_length=500, blank=True, null=True, default=None, verbose_name="User Biography")
    location = models.CharField(max_length=30, blank=True, null=True, default=None, verbose_name="Current Location")
    birth_date = models.DateField(blank=True, null=True, default=None, verbose_name="Birth Date")
    nickname = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="Nickname")
    aliases = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name="Aliases")
    suffix = models.CharField(max_length=55, null=True, blank=True, verbose_name="Suffix")
    notes = models.TextField(max_length=255, null=True, blank=True, verbose_name="Notes")
    created = models.DateTimeField(_("Creation date and time"),editable=False,)
    modified = models.DateTimeField(_("Modification date and time"),null=True,editable=False,)
    
    # Detail Fields
    
    # Personal Fields
    gender = models.CharField(max_length=55, null=True, blank=True, verbose_name="Gender")
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
    address = models.ManyToManyField(Address, verbose_name="Address")
    telephone = models.ManyToManyField(Telephone, verbose_name="Telephone")
    email = models.ManyToManyField(Email, verbose_name="Email")
    website = models.ManyToManyField(Website, verbose_name="Website")
    #social = models.ManyToManyField(Social, verbose_name="Social")

    # Other Fields
    prefix = models.ForeignKey(Prefix, on_delete=models.DO_NOTHING, null=True, blank=True)
    type = models.ForeignKey(UserType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Type")
    status = models.ForeignKey(UserStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Status")
    classification = models.ForeignKey(UserClassification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Classification")
    category = models.ForeignKey(UserCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Category")
    authorisation = models.ForeignKey(UserAuthorisation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Person Authorisation")
    
    # Auto Fields
    slug_first = models.SlugField(editable=False, null=True, blank=True, verbose_name="First Name Slug")
    slug_last = models.SlugField(editable=False, null=True, blank=True, verbose_name="Last Name Slug")
    slug_middle = models.SlugField(editable=False, null=True, blank=True, verbose_name="Middle Name Slug")

    class Meta:
        verbose_name_plural = _("Profiles")
        
    def __str__(self):
        return "%s, %s" % (self.user.last_name,self.user.first_name)
    
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
        return reverse('user')
    
    def save(self,force_insert=False, force_update=False):
        from django.template.defaultfilters import slugify
        if not self.slug_last:
            self.slug_last = slugify(self.user.last_name)
        if not self.slug_first:
            self.slug_first = slugify(self.user.first_name)
        if not self.pk:
           self.created = timezone_now()
        else:
            if not self.created:
                self.created = timezone_now()
            self.modified = timezone_now()
        models.Model.save(self,force_insert,force_update)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
