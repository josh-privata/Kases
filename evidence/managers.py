### Evidence Managers ##

#from django.db import models

#class CaseQuerySet(models.QuerySet):
    
#    def count_cases(self):
#        return self.objects.count()

#    def active(self):
#        return self.filter(status__title__icontains='active')

#    def inactive(self):
#        return self.filter(status__title__icontains='inactive')


#class CaseManager(models.Manager):

#    def get_queryset(self):
#        return CaseQuerySet(self.model, using=self._db)
    
#    def count_cases(self):
#        return self.get_queryset().count()
  
