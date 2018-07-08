from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from task.models import TaskPriority
from task.models import TaskType
#from case.models import CaseTask
from case.models import Case
from case.models import CaseAuthorisation
from case.models import CaseClassification
from case.models import CaseType
from case.models import CasePriority
from case.models import CaseStatus
from case.models import CaseStatusGroup
from evidence.models import EvidenceType
from evidence.models import ChainOfCustody
from user.models import Profile
from configuration.models import Options
from simple_history.admin import SimpleHistoryAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Options)
admin.site.register(EvidenceType)
admin.site.register(ChainOfCustody)
admin.site.register(CaseAuthorisation)
admin.site.register(CaseClassification)
admin.site.register(CaseType)
admin.site.register(CasePriority)
admin.site.register(CaseStatus)
admin.site.register(CaseStatusGroup)
admin.site.register(Case, SimpleHistoryAdmin)
#admin.site.register(CaseTask)
admin.site.register(TaskPriority)
admin.site.register(TaskType)
