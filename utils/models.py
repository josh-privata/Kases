## Model Mixins ##

## python imports
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from django.db import models
#from django.contrib.sites.models import Site
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic.base import ContextMixin
from simple_history.models import HistoricalRecords


class MultipleFormsMixin(ContextMixin):
    """
    A mixin that provides a way to show and handle multiple forms in a request.
    It's almost fully-compatible with regular FormsMixin
    """

    initial = {}
    forms_classes = [ ]
    success_url = None
    prefix = None
    active_form_keyword = "selected_form"

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_prefix(self):
        """
        Returns the prefix to use for forms on this view
        """
        return self.prefix

    def get_forms_classes(self):
        """
        Returns the forms classes to use in this view
        """
        return self.forms_classes

    def get_active_form_number(self):
        """
        Returns submitted form index in available forms list
        """
        if self.request.method in ('POST', 'PUT'):
            try:
                return int(self.request.POST[self.active_form_keyword])
            except (KeyError, ValueError):
                raise ImproperlyConfigured("You must include hidden field with field index in every form!")

    def get_forms(self, active_form = None):
        """
        Returns instances of the forms to be used in this view.
        Includes provided `active_form` in forms list.
        """
        all_forms_classes = self.get_forms_classes()
        all_forms = [
            form_class(**self.get_form_kwargs()) 
            for form_class in all_forms_classes]
        if active_form:
            active_form_number = self.get_active_form_number()
            all_forms[active_form_number] = active_form
        return all_forms

    def get_form(self):
        """
        Returns active form. Works only on `POST` and `PUT`, otherwise returns None.
        """
        active_form_number = self.get_active_form_number()
        if active_form_number is not None:            
            all_forms_classes = self.get_forms_classes()
            active_form_class = all_forms_classes[active_form_number]
            return active_form_class(**self.get_form_kwargs(is_active=True))

    def get_form_kwargs(self, is_active = False):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if is_active:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return url

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(self.get_context_data(active_form=form))

    def get_context_data(self, **kwargs):
        """
        Insert the forms into the context dict.
        """
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms(kwargs.get('active_form'))
        return super(MultipleFormsMixin, self).get_context_data(**kwargs)


class UrlMixin(models.Model):
    """
    A replacement for get_absolute_url()
    Models extending this mixin should have
    either get_url or get_url_path implemented.
    
    -- Template Usage -- 
    When you need a link of an object in the same website use;
        <a href="{{ model.get_url_path }}">{{ model.title }}<a>
    For the links in e-mails, RSS feeds, or APIs use;
        <a href="{{ model.get_url }}">{{ model.title }}</a>
    """
    class Meta:
        abstract = True
    
    def get_url(self):
        if hasattr(self.get_url_path, "dont_recurse"):
            raise NotImplementedError
        try:
            path = self.get_url_path()
        except NotImplementedError:
            raise
        website_url = getattr(settings, "DEFAULT_WEBSITE_URL", "http://127.0.0.1:8000")
        return website_url + path
    get_url.dont_recurse = True

    def get_url_path(self):
        if hasattr(self.get_url, "dont_recurse"):
            raise NotImplementedError
        try:
            url = self.get_url()
        except NotImplementedError:
            raise
        bits = urlparse.urlparse(url)
        return urlparse.urlunparse(("", "") + bits[2:])
    get_url_path.dont_recurse = True

    def get_absolute_url(self):
        return self.get_url_path()


class ObjectDescriptionMixin(models.Model):
    """
    Abstract base class for most models.

    :description (optional): Description
    :private (optional): Is it private Boolean
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 

    """

    description = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Description")
    created = models.DateTimeField(_("Creation date and time"),editable=False,)
    modified = models.DateTimeField(_("Modification date and time"),null=True,editable=False,)
    private = models.BooleanField(default=False, blank=True, verbose_name="Private")
    #created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created by', null=True, blank=True, editable=False, verbose_name="Created By")
    #modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='modified by', null=True, blank=True, editable=False, verbose_name="Modified By")
        
    def save(self, *args, **kwargs):
        if not self.pk:
           self.created = timezone_now()
           #self.created_by = request.user
        else:
            if not self.created:
                self.created = timezone_now()
            self.modified = timezone_now()
            #if not self.created_by:
            #    self.created_by = request.user
            #self.modified_by = request.user
        super(ObjectDescriptionMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Authorisation(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an object authorisation.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """

    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Authorisation")

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.title
    

class Classification(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an object classification.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """

    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Classification")
    
    class Meta:
        abstract = True
        verbose_name = _('Classification')
        verbose_name_plural = _('Classifications')

    #def get_absolute_url(self):
    #    return reverse('classification_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class Type(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an object type.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """

    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Type")
    
    class Meta:
        abstract = True
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    #def get_absolute_url(self):
    #    return reverse('type_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class Priority(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an object priority.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """

    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Priority")
    colour = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Colour")
    #action_delta_hours = models.IntegerField(blank=True, null=True, default=None, verbose_name="Action Delta Days")
   
    class Meta:
        abstract = True
        verbose_name = _('Priority')
        verbose_name_plural = _('Priorities')

    #def get_absolute_url(self):
    #    return reverse('priority_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class Category(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an object category.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    
    """
    
    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Category")
    
    class Meta:
        abstract = True
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    #def get_absolute_url(self):
    #    return reverse('category_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class Status(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an object status.

    :title (optional): Title
    :description (optional): Description
    :private (optional): Is it private Boolean
    :colour (optional): Colour representation
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model
    
    """

    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Status")

    class Meta:
        abstract = True
        verbose_name = _('Status')
        verbose_name_plural = _('Status')

    #def get_absolute_url(self):
    #    return reverse('status_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class StatusGroup(ObjectDescriptionMixin):
    """
    Abstract model to contain information about an object status group.

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

    # General Fields
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name="Status Group")

    class Meta:
        abstract = True
        verbose_name = _('Status Group')
        verbose_name_plural = _('Status Groups')

    #def get_absolute_url(self):
    #    return reverse('statusgroup_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s' % self.title


class UploadModel(ObjectDescriptionMixin):
    """
    Abstract model to contain information about a file upload.

    :date_time (optional):
    :file_note (optional):
    :file_hash (optional):
    :file_name (optional):
    :upload_location (optional):
    :file_title (optional):
    :created_by (optional):
    :deleted (optional):
    :date_deleted (optional):
    :description (optional): Description
    :private (optional): Is it private Boolean
    :created (auto): Date Created
    :modified (auto): Date Modified
    :created_by (auto): Created by linked User model  
    :modified_by (auto): Modified by linked User model 
    
    """

    # General Fields
    date_time = models.DateTimeField(auto_now=True, null=True)
    file_note = models.CharField(max_length=250, blank=True, null=True, default=None)
    file_hash = models.CharField(max_length=250, blank=True, null=True, default=None)
    file_name = models.CharField(max_length=250, blank=True, null=True, default=None)
    upload_location = models.CharField(max_length=250, blank=True, null=True, default=None)
    file_title = models.CharField(max_length=250, blank=True, null=True, default=None)
    deleted = models.BooleanField(default=False, blank=True)
    date_deleted = models.DateTimeField(auto_now=True, null=True)
  
    @property
    def file_path(self):
        return path.join(self.upload_location, self.file_name)

    

#class ForemanOptions(Model):
#    __tablename__ = 'options'
#    id = Column(Integer, primary_key=True)
#    date_format = models.CharField(max_length=250, blank=True, null=True, default=None)
#    default_location = models.CharField(max_length=250, blank=True, null=True, default=None)
#    case_names = models.CharField(max_length=250, blank=True, null=True, default=None)
#    c_increment = Column(Integer)
#    c_leading_zeros = Column(Integer)
#    c_leading_date = models.CharField(max_length=250, blank=True, null=True, default=None)
#    c_list_name = models.CharField(max_length=250, blank=True, null=True, default=None)
#    task_names = models.CharField(max_length=250, blank=True, null=True, default=None)
#    t_increment = Column(Integer)
#    t_leading_zeros = Column(Integer)
#    t_list_name = models.CharField(max_length=250, blank=True, null=True, default=None)
#    company = models.CharField(max_length=250, blank=True, null=True, default=None)
#    department = models.CharField(max_length=250, blank=True, null=True, default=None)
#    date_created = models.DateTimeField(auto_now=True, null=True)
#    over_limit_case = models.BooleanField(default=False, blank=True)
#    over_limit_task = models.BooleanField(default=False, blank=True)
#    auth_view_tasks = models.BooleanField(default=False, blank=True)
#    auth_view_evidence = models.BooleanField(default=False, blank=True)
#    manager_inherit = models.BooleanField(default=False, blank=True)
#    evidence_retention_period = Column(Integer)
#    evidence_retention = models.BooleanField(default=False, blank=True)
#    email_alert_all_inv_task_queued = models.BooleanField(default=False, blank=True)
#    email_alert_inv_assigned_task = models.BooleanField(default=False, blank=True)
#    email_alert_qa_assigned_task = models.BooleanField(default=False, blank=True)
#    email_alert_caseman_inv_self_assigned = models.BooleanField(default=False, blank=True)
#    email_alert_caseman_qa_self_assigned = models.BooleanField(default=False, blank=True)
#    email_alert_req_task_completed = models.BooleanField(default=False, blank=True)
#    email_alert_case_man_task_completed = models.BooleanField(default=False, blank=True)
#    email_alert_all_caseman_new_case = models.BooleanField(default=False, blank=True)
#    email_alert_all_caseman_case_auth = models.BooleanField(default=False, blank=True)
#    email_alert_req_case_caseman_assigned = models.BooleanField(default=False, blank=True)
#    email_alert_req_case_opened = models.BooleanField(default=False, blank=True)
#    email_alert_req_case_closed = models.BooleanField(default=False, blank=True)
#    email_alert_req_case_archived = models.BooleanField(default=False, blank=True)
#    email_alert_caseman_requester_add_task = models.BooleanField(default=False, blank=True)
#    number_logins_before_account_lockout = Column(Integer)

#    CASE_NAME_OPTIONS = ['NumericIncrement', 'DateNumericIncrement', 'FromList']
#    TASK_NAME_OPTIONS = ['NumericIncrement', 'FromList', 'TaskTypeNumericIncrement']
#    ACCOUNT_LOCKOUT = [("No lockout", "None"), ("1 attempt", "1"), ("2 attempts", "2"), ("3 attempts", "3"),
#                       ("4 attempts", "4"), ("5 attempts", "5")]

#    def __init__(self, date_format, default_location, case_names, task_names, company, department, c_list_location=None,
#                 c_leading_zeros=3, t_list_location=None, t_leading_zeros=3, auth_view_tasks=True,
#                 auth_view_evidence=True, manager_inherit=False):
#        self.date_format = date_format
#        self.default_location = default_location
#        self.case_names = case_names
#        self.c_increment = -1
#        self.c_leading_zeros = c_leading_zeros
#        self.c_leading_date = datetime.now().strftime("%Y%m%d")
#        self.c_list_name = self.import_list(c_list_location)
#        self.task_names = task_names
#        self.t_increment = -1
#        self.t_leading_zeros = t_leading_zeros
#        self.t_list_name = self.import_list(t_list_location)
#        self.company = company
#        self.department = department
#        self.date_created = datetime.now()
#        self.over_limit_case = False
#        self.over_limit_task = False
#        self.auth_view_evidence = auth_view_evidence
#        self.auth_view_tasks = auth_view_tasks
#        self.manager_inherit = manager_inherit
#        self.evidence_retention = False
#        self.evidence_retention_period = None

#        TaskCategory.populate_default()
#        TaskType.populate_default()
#        EvidenceType.populate_default()
#        CaseClassification.populate_default()
#        CaseType.populate_default()
#        CasePriority.populate_default()

#        self.email_alert_all_inv_task_queued = False
#        self.email_alert_inv_assigned_task = False
#        self.email_alert_qa_assigned_task = False
#        self.email_alert_caseman_inv_self_assigned = False
#        self.email_alert_caseman_qa_self_assigned = False
#        self.email_alert_req_task_completed = False
#        self.email_alert_case_man_task_completed = False
#        self.email_alert_all_caseman_new_case = False
#        self.email_alert_all_caseman_case_auth = False
#        self.email_alert_req_case_caseman_assigned = False
#        self.email_alert_req_case_opened = False
#        self.email_alert_req_case_closed = False
#        self.email_alert_req_case_archived = False
#        self.email_alert_caseman_requester_add_task = False
#        self.number_logins_before_account_lockout = None

#    @staticmethod
#    def import_list(list_location):
##        if list_location is not None:
##            unique = datetime.now().strftime("%H%M%S-%d%m%Y-%f")
##            filename, ext = path.splitext(path.basename(list_location))
##            full_filename = "{}_{}{}".format(filename, unique, ext)
##            destination = path.join(ROOT_DIR, 'files', full_filename)
##            shutil.copy(list_location, destination)
##            return destination
#        pass

#    @staticmethod
#    def import_names(type_list, list_location):
##        options = session.query(ForemanOptions).first()
##        count = options.check_list_valid(list_location)
##        if count:
##            dest = options.import_list(list_location)
##            # reset
##            if type_list == "case":
##                options.c_increment = -1
##                options.c_list_name = dest
##                options.over_limit_case = False
##            elif type_list == "task":
##                options.t_increment = -1
##                options.t_list_name = dest
##                options.over_limit_task = False
##        return count
#        pass

#    @staticmethod
#    def check_list_valid(list_location):
##        try:
##            with open(list_location, "r") as names:
##                contents = names.readlines()
##            return len(contents)
##        except Exception:
##            # catch all!
##            return None
#        pass

#    @staticmethod
#    def get_number_logins_before_account_lockout():
##        options = session.query(ForemanOptions).first()
##        return options.number_logins_before_account_lockout
#        pass

#    @staticmethod
#    def get_number_logins_before_account_lockout_form():
##        options = session.query(ForemanOptions).first()
##        return str(options.number_logins_before_account_lockout)
#        pass

#    @staticmethod
#    def update_number_logins_before_account_lockout(num_logins):
##        options = session.query(ForemanOptions).first()
##        options.number_logins_before_account_lockout = num_logins
#        pass

#    @staticmethod
#    def get_date(date):
##        options = session.query(ForemanOptions).first()
##        date_format = options.date_format
##        return date.strftime(date_format)
#        pass

#    @staticmethod
#    def get_default_location():
##        options = session.query(ForemanOptions).first()
##        return options.default_location
#        pass

#    @staticmethod
#    def get_date_created():
##        options = session.query(ForemanOptions).first()
##        return options.date_created
#        pass

#    @staticmethod
#    def get_evidence_retention_period():
##        options = session.query(ForemanOptions).first()
##        return options.evidence_retention, options.evidence_retention_period
#        pass

#    @staticmethod
#    def run_out_of_names():
##        options = session.query(ForemanOptions).first()
##        return [options.over_limit_task and options.task_names == "FromList",
##                options.over_limit_case and options.case_names == "FromList"]
#        pass

#    @staticmethod
#    def get_next_case_name(test=False):
##        options = session.query(ForemanOptions).first()
##        if options.case_names == 'NumericIncrement':
##            options.c_increment += 1
##            return '{num:0{width}}'.format(num=options.c_increment, width=options.c_leading_zeros)
##        elif options.case_names == "DateNumericIncrement":
##            now = datetime.now().strftime("%Y%m%d")
##            if now == options.c_leading_date:
##                options.c_increment += 1
##                return '{now}{num:0{width}}'.format(now=now, num=options.c_increment, width=options.c_leading_zeros)
##            else:
##                options.c_increment = 1
##                options.c_leading_date = now
##                return '{now}{num:0{width}}'.format(now=now, num=options.c_increment, width=options.c_leading_zeros)
##        elif options.case_names == "FromList":
##            options.c_increment += 1
##            return ForemanOptions.get_next_case_name_from_list(options.c_list_name, options.c_increment,
##                                                               options, "c", test)
#        pass

#    @staticmethod
#    def get_next_task_name(case, tasktype=None, test=False):
##        options = session.query(ForemanOptions).first()
##        if case is not None:
##            options.t_increment = len(case.tasks)
##        else:
##            options.t_increment = -1
##        if options.task_names == 'NumericIncrement':
##            options.t_increment += 1
##            return '{case}_{num1:0{width1}}'.format(case=case.case_name, num1=options.t_increment,
##                                                    width1=options.t_leading_zeros)
##        elif options.task_names == "FromList":
##            options.t_increment += 1
##            return ForemanOptions.get_next_case_name_from_list(options.t_list_name, options.t_increment,
##                                                               options, "t", test)
##        elif options.task_names == "TaskTypeNumericIncrement":
##            options.t_increment += 1
##            return '{task}_{num1:0{width1}}'.format(task=tasktype, num1=options.t_increment,
##                                                    width1=options.t_leading_zeros)
#        pass

#    @staticmethod
#    def get_next_case_name_from_list(filename, increment, options, content_type, test):

##        if filename is None:
##            results = '{num:0{width}}'.format(num=options.c_increment, width=options.c_leading_zeros)
##            if content_type == "t":
##                options.over_limit_task = True
##            elif content_type == "c":
##                options.over_limit_case = True
##            return results

##        with open(filename, 'r') as contents:
##            all_content = contents.readlines()
##            try:
##                results = all_content[increment].strip()
##                if test is True:
##                # if it's a test, and there is actually a next one; then reverse the increment otherwise
##                # using one for no reason
##                    if content_type == "t":
##                        options.t_increment -= 1
##                    elif content_type == "c":
##                        options.c_increment -= 1
##            except IndexError:
##                results = '{num:0{width}}'.format(num=options.c_increment, width=options.c_leading_zeros)
##                if content_type == "t":
##                    options.over_limit_task = True
##                elif content_type == "c":
##                    options.over_limit_case = True
##        return results
#        pass

#    @staticmethod
#    def get_options():
##        return session.query(ForemanOptions).first()
#        pass

#    @staticmethod
#    def set_options(company, department, folder, date_display, case_names, task_names):
##        opt = ForemanOptions.get_options()
##        opt.company = company
##        opt.department = department
##        opt.default_location = folder
##        opt.date_format = date_display
##        opt.case_names = case_names
##        opt.task_names = task_names
#        pass



#class MetaTagsMixin(models.Model):
#    """
#    Abstract base class for meta tags in the <head> section
#    """
#    meta_keywords = models.CharField(_("Keywords"), max_length=255, blank=True, help_text=_("Separate keywords by comma."),)
#    meta_description = models.CharField(_("Description"), max_length=255, blank=True,)
#    meta_author = models.CharField(_("Author"), max_length=255, blank=True,)
#    meta_copyright = models.CharField(_("Copyright"), max_length=255, blank=True,)

#    class Meta:
#        abstract = True
#        def get_meta_keywords(self):
#            tag = ""
#            if self.meta_keywords:
#                tag = '<meta name="keywords" content="%s" />\n' % escape(self.meta_keywords)
#            return mark_safe(tag)
        
#        def get_meta_description(self):
#            tag = ""
#            if self.meta_description:
#                tag = '<meta name="description" content="%s" />\n' % escape(self.meta_description)
#            return mark_safe(tag)

#        def get_meta_author(self):
#            tag = ""
#            if self.meta_author:
#                tag = '<meta name="author" content="%s" />\n' % escape(self.meta_author)
#            return mark_safe(tag)
        
#        def get_meta_copyright(self):
#            tag = ""
#            if self.meta_copyright:
#                tag = '<meta name="copyright" content="%s" />\n' % escape(self.meta_copyright)
#            return mark_safe(tag)
        
#        def get_meta_tags(self):
#            return mark_safe("".join((self.get_meta_keywords(), self.get_meta_description(),self.get_meta_author(), self.get_meta_copyright(),)))