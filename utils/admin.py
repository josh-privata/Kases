from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from task.models import *
from case.models import *
from evidence.models import *
from note.models import *
from event.models import *
from entity.models.person import *
from entity.models.company import *
from inventory.models import *
from user.models import Profile
#from configuration.models import Options
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
#admin.site.register(Options)

# Entity
admin.site.register(PersonAuthorisation, SimpleHistoryAdmin)
admin.site.register(PersonClassification, SimpleHistoryAdmin)
admin.site.register(PersonType, SimpleHistoryAdmin)
admin.site.register(PersonCategory, SimpleHistoryAdmin)
admin.site.register(PersonStatus, SimpleHistoryAdmin)
admin.site.register(PersonStatusGroup, SimpleHistoryAdmin)
admin.site.register(Person, SimpleHistoryAdmin)
admin.site.register(CompanyAuthorisation, SimpleHistoryAdmin)
admin.site.register(CompanyClassification, SimpleHistoryAdmin)
admin.site.register(CompanyType, SimpleHistoryAdmin)
admin.site.register(CompanyCategory, SimpleHistoryAdmin)
admin.site.register(CompanyStatus, SimpleHistoryAdmin)
admin.site.register(CompanyStatusGroup, SimpleHistoryAdmin)
admin.site.register(Company, SimpleHistoryAdmin)

# Event
admin.site.register(EventAuthorisation, SimpleHistoryAdmin)
admin.site.register(EventClassification, SimpleHistoryAdmin)
admin.site.register(EventType, SimpleHistoryAdmin)
admin.site.register(EventPriority, SimpleHistoryAdmin)
admin.site.register(EventCategory, SimpleHistoryAdmin)
admin.site.register(EventStatus, SimpleHistoryAdmin)
admin.site.register(EventStatusGroup, SimpleHistoryAdmin)

# Evidence
admin.site.register(EvidenceAuthorisation, SimpleHistoryAdmin)
admin.site.register(EvidenceClassification, SimpleHistoryAdmin)
admin.site.register(EvidenceType, SimpleHistoryAdmin)
admin.site.register(ChainOfCustody, SimpleHistoryAdmin)
admin.site.register(EvidencePriority, SimpleHistoryAdmin)
admin.site.register(EvidenceCategory, SimpleHistoryAdmin)
admin.site.register(EvidenceStatus, SimpleHistoryAdmin)
admin.site.register(EvidenceStatusGroup, SimpleHistoryAdmin)

# Task
admin.site.register(TaskAuthorisation, SimpleHistoryAdmin)
admin.site.register(TaskClassification, SimpleHistoryAdmin)
admin.site.register(TaskType, SimpleHistoryAdmin)
admin.site.register(TaskPriority, SimpleHistoryAdmin)
admin.site.register(TaskCategory, SimpleHistoryAdmin)
admin.site.register(TaskStatus, SimpleHistoryAdmin)
admin.site.register(TaskStatusGroup, SimpleHistoryAdmin)

# Note
admin.site.register(NoteAuthorisation, SimpleHistoryAdmin)
admin.site.register(NoteClassification, SimpleHistoryAdmin)
admin.site.register(NoteType, SimpleHistoryAdmin)
admin.site.register(NotePriority, SimpleHistoryAdmin)
admin.site.register(NoteCategory, SimpleHistoryAdmin)
admin.site.register(NoteStatus, SimpleHistoryAdmin)
admin.site.register(NoteStatusGroup, SimpleHistoryAdmin)

# Case
admin.site.register(CaseAuthorisation, SimpleHistoryAdmin)
admin.site.register(CaseClassification, SimpleHistoryAdmin)
admin.site.register(CaseType, SimpleHistoryAdmin)
admin.site.register(CasePriority, SimpleHistoryAdmin)
admin.site.register(CaseCategory, SimpleHistoryAdmin)
admin.site.register(CaseStatus, SimpleHistoryAdmin)
admin.site.register(CaseStatusGroup, SimpleHistoryAdmin)
admin.site.register(CaseTask, SimpleHistoryAdmin)
admin.site.register(CaseNote, SimpleHistoryAdmin)
admin.site.register(CaseEvidence, SimpleHistoryAdmin)
admin.site.register(CasePerson, SimpleHistoryAdmin)
admin.site.register(CaseCompany, SimpleHistoryAdmin)
admin.site.register(CaseInventory, SimpleHistoryAdmin)
admin.site.register(CaseEvent, SimpleHistoryAdmin)
admin.site.register(EventPerson, SimpleHistoryAdmin)
admin.site.register(EventCompany, SimpleHistoryAdmin)


#admin.site.register(ContactLocation)
#admin.site.register(Country)
#admin.site.register(State)
#admin.site.register(Address)
#admin.site.register(Telephone)
#admin.site.register(Email)
#admin.site.register(Website)
#admin.site.register(Prefix)
#admin.site.register(Person)

