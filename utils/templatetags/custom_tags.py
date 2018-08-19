## Custom Template Tags ##

import re
from datetime import datetime
from django import template
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as tz_now


register = template.Library()


### FILTERS ###
@register.filter
def time_since(value):
    """ 
    Returns number of days between today and value.
    
    USAGE: 
        {% load custom_tags %}
        {{ object.<<object>> | time_since }}
    """
    today = tz_now().date()
    if isinstance(value, datetime.datetime):
        value = value.date()
        diff = today - value
    if diff.days > 1:
        return _("%s days ago") % diff.days
    elif diff.days == 1:
        return _("yesterday")
    elif diff.days == 0:
        return _("today")
    else:
        # Date is in the future; return formatted date.
        return value.strftime("%B %d, %Y")


@register.filter
def shorten_url(url, letter_count):
    """ 
    Returns a shortened human-readable URL.
    Follow the command with :x where x is the maximumn numnber of chars

    USAGE:
        {% load custom_tags %}
        {{ object.website|shorten_url:30 }}

    """
    letter_count = int(letter_count)
    re_start = re.compile(r"^https?://")
    re_end = re.compile(r"/$")
    url = re_end.sub("", re_start.sub("", url))
    if len(url) > letter_count:
        url = "%s…" % url[:letter_count - 1]
    return url


### TAGS ###
@register.tag
def get_objects(parser, token):
    """ 
    Gets a queryset of objects of the model specified by app and model names

    USAGE:
        {% load custom_tags %}
        {% get_objects [<manager>.]<method> from <app_name>.<model_name> [limit <amount>] as <var_name> %}

    Example:
        {% get_objects latest_published from people.Person limit 3 as people %}
        {% get_objects site_objects.all from news.Article limit 3 as articles %}
        {% get_objects site_objects.all from news.Article as articles %}

    """
    amount = None
    try:
        tag_name, manager_method, str_from, appmodel, str_limit, amount, str_as, var_name =  token.split_contents()
    except ValueError:
        try:
            tag_name, manager_method, str_from, appmodel, str_as, var_name = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError
                #"get_objects tag requires a following "\
                #"syntax: " \
                #"{% get_objects [<manager>.]<method> "\
                #"from <app_ name>.<model_name> "\
                #"[limit <amount>] as <var_name> %}"
    try:
        app_name, model_name = appmodel.split(".")
    except ValueError:
        raise template.TemplateSyntaxError
            #"get_objects tag requires application name and model name separated by a dot"
    model = models.get_model(app_name, model_name)
    return ObjectsNode(model, manager_method, amount, var_name)


class ObjectsNode(template.Node):
    def __init__(self, model, manager_method, amount, var_name):
        self.model = model
        self.manager_method = manager_method
        self.amount = amount
        self.var_name = var_name

    def render(self, context):
        if "." in self.manager_method:
            manager, method = self.manager_method.split(".")
        else:
            manager = "_default_manager"
            method = self.manager_method
            qs = getattr(getattr(self.model, manager),method,self.model._default_manager.none,)()
        if self.amount:
            amount = template.resolve_variable(self.amount, context)
            context[self.var_name] = qs[:amount]
        else:
            context[self.var_name] = qs
        return ""