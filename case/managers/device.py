## Case Managers ##
import datetime
from django.db import models

class CaseQuerySet(models.QuerySet):
    """ Contains predefined queries for Device Model.

    Args:
        title (str) [128]: Title for the Task 


    """

    def active(self):
        return self.filter(status__title__icontains='active')

    def inactive(self):
        return self.filter(status__title__icontains='inactive')

    def overdue(self):
        return self.filter(deadline__lt=datetime.datetime.now())

    def due_today(self):
        return self.filter(deadline__eq=datetime.datetime.now())

    def is_private(self):
        return self.filter(private__eq=True)

    def is_assigned(self):
        return self.filter(assigned_to__null=False)


class CaseManager(models.Manager):
    """ Manages predefined queries for Device Model.

    Args:
        title (str) [128]: Title for the Task 


    """

    def get_queryset(self):
        return CaseQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()
    
    def overdue(self):
        return self.get_queryset().overdue()  

    def due_today(self):
        return self.get_queryset().due_today()

    def is_private(self):
        return self.get_queryset().is_private()

    def is_assigned(self):
        return self.get_queryset().is_assigned()