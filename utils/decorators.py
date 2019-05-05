from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

# Usage in classes
#from django.utils.decorators import method_decorator
#from django.contrib.auth.decorators import login_required
#from ..decorators import student_required
# @method_decorator([login_required, student_required], name='dispatch')

# Usage in functions
#from django.contrib.auth.decorators import login_required
#from django.shortcuts import get_object_or_404, render
#from utils.decorators import student_required
#@login_required
#@student_required


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# Usage
#from .mixins import GroupRequiredMixin
#from django.views.generic import View

#class DemoView(GroupRequiredMixin, View):
#  group_required = [u'admin', u'manager']
  
#  # View code...

class GroupRequiredMixin(object):
    """
        group_required - list of strings, required param
    """

    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied
        else:
            user_groups = []
            for group in request.user.groups.values_list('name', flat=True):
                user_groups.append(group)
            if len(set(user_groups).intersection(self.group_required)) <= 0:
                raise PermissionDenied
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)