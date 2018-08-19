"""
Definition of urls for Kases.
"""


from datetime import datetime
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views
#import base.forms
#import base.views
#from evidence.views import EvidenceList, EvidenceCreate, EvidenceTable, EvidenceDelete
#from evidence.views import EvidenceUpdate, EvidenceHome, EvidenceDetail
#from note.views import NoteList, NoteCreate, NoteTable, NoteDelete
#from note.views import  NoteUpdate, NoteHome, NoteDetail
#from task.views import TaskList, TaskCreate, TaskTable, TaskDelete
#from task.views import TaskUpdate, TaskHome, TaskDetail
from case.views import CaseList, CaseCreate, CaseTable, CaseDelete
from case.views import CaseUpdate, CaseHome, CaseDetail, case_table
from case.views import CaseNoteUpdate, CaseNoteDetail, CaseNoteDelete
from case.views import CaseNoteCreate, CaseNoteList, CaseNoteHome
from case.views import CaseEventUpdate, CaseEventDetail, CaseEventDelete
from case.views import CaseEventCreate, CaseEventList, create_event, CaseEventHome
from case.views import CaseEvidenceUpdate, CaseEvidenceDetail, CaseEvidenceDelete
from case.views import CaseEvidenceCreate, CaseEvidenceList, CaseEvidenceHome
from case.views import CaseTaskUpdate, CaseTaskDetail, CaseTaskDelete
from case.views import CaseTaskCreate, CaseTaskList, CaseTaskHome
from case.views import CaseDeviceUpdate, CaseDeviceDetail, CaseDeviceDelete
from case.views import CaseDeviceCreate, CaseDeviceHome
from case.views import CasePersonCreate, CasePersonUpdate, CaseEntityHome
from case.views import CasePersonDetail, CasePersonDelete
from case.views import CaseCompanyCreate, CaseCompanyUpdate
from case.views import CaseCompanyDetail, CaseCompanyDelete
from inventory.views import InventoryHome, DeviceCreate, DeviceDetail, DeviceUpdate, DeviceDelete
from loan.views import LoanHome, LoanCreate, LoanDetail, LoanUpdate, LoanDelete
#from inventory.views import DevicesListView, HeadphonesDetail, AdapterDetail, DeviceAdd
#from inventory.views import IpadUpdate, HeadphonesUpdate, AdapterUpdate, DeviceDelete, AdapterCommentUpdate
#from inventory.views import IpadCommentDelete, IpadCommentUpdate, HeadphonesCommentDelete, HeadphonesCommentUpdate, AdapterCommentDelete
#from entity.views.company import list, detail, create, update, delete
from entity.views.person import person_delete, person_update, person_detail, person_add
from entity.views.company import company_delete, company_edit, company_detail, company_add
from entity.views.entity import EntityHome
from utils.forms import BootstrapAuthenticationForm



admin.autodiscover()


urlpatterns = [

    # Case
    path('case/', CaseHome.as_view(), name='cases'), 
    path('case/create/', CaseCreate.as_view(), name='case_create'),
    path('case/<int:pk>/', CaseDetail.as_view(), name='case_detail'),
    path('case/<int:pk>/update/', CaseUpdate.as_view(), name='case_edit'),
    path('case/<int:pk>/delete/', CaseDelete.as_view(), name='case_delete'),
    # Case Display
    path('case/list/', CaseList.as_view(), name='case_list'),
    path('case/table/', CaseTable.as_view(), name='casetable'),
    path('case/table1/', case_table, name='case_table'),
    # Case Notes
    path('case/<int:casepk>/note/', CaseNoteHome.as_view(), name='casenote'),
    path('case/<int:casepk>/note/create/', CaseNoteCreate.as_view(), name='casenote_create'),
    path('case/<int:casepk>/note/<int:pk>/', CaseNoteDetail.as_view(), name='casenote_detail'),
    path('case/<int:casepk>/note/<int:pk>/update/', CaseNoteUpdate.as_view(), name='casenote_update'),
    path('case/<int:casepk>/note/<int:pk>/delete/', CaseNoteDelete.as_view(), name='casenote_delete'),
    path('case/<int:casepk>/note/list/', CaseNoteList.as_view(), name='casenote_list'),
    # Case Events
    path('case/<int:casepk>/event/', CaseEventHome.as_view(), name='caseevent'),
    path('case/<int:casepk>/event/create/', CaseEventCreate.as_view(), name='caseevent_create'),
    path('case/<int:casepk>/event/create1/', create_event, name='caseevent_create1'),
    path('case/<int:casepk>/event/<int:pk>/', CaseEventDetail.as_view(), name='caseevent_detail'),
    path('case/<int:casepk>/event/<int:pk>/update/', CaseEventUpdate.as_view(), name='caseevent_update'),
    path('case/<int:casepk>/event/<int:pk>/delete/', CaseEventDelete.as_view(), name='caseevent_delete'),
    path('case/<int:casepk>/event/list/', CaseEventList.as_view(), name='caseevent_list'),
    # Case Evidence
    path('case/<int:casepk>/evidence/', CaseEvidenceHome.as_view(), name='caseevidence'),
    path('case/<int:casepk>/evidence/create/', CaseEvidenceCreate.as_view(), name='caseevidence_create'),
    path('case/<int:casepk>/evidence/<int:pk>/', CaseEvidenceDetail.as_view(), name='caseevidence_detail'),
    path('case/<int:casepk>/evidence/<int:pk>/update/', CaseEvidenceUpdate.as_view(), name='caseevidence_update'),
    path('case/<int:casepk>/evidence/<int:pk>/delete/', CaseEvidenceDelete.as_view(), name='caseevidence_delete'),
    path('case/<int:casepk>/evidence/list/', CaseEvidenceList.as_view(), name='caseevidence_list'),
    # Case Tasks
    path('case/<int:casepk>/task/', CaseTaskHome.as_view(), name='casetask'),
    path('case/<int:casepk>/task/create/', CaseTaskCreate.as_view(), name='casetask_create'),
    path('case/<int:casepk>/task/<int:pk>/', CaseTaskDetail.as_view(), name='casetask_detail'),
    path('case/<int:casepk>/task/<int:pk>/update/', CaseTaskUpdate.as_view(), name='casetask_update'),
    path('case/<int:casepk>/task/<int:pk>/delete/', CaseTaskDelete.as_view(), name='casetask_delete'),
    path('case/<int:casepk>/task/list/', CaseTaskList.as_view(), name='casetask_list'),
    # Case Devices
    path('case/<int:casepk>/device/', CaseDeviceHome.as_view(), name='casedevice'),
    path('case/<int:casepk>/device/create/', CaseDeviceCreate.as_view(), name='casedevice_create'),
    path('case/<int:casepk>/device/<int:pk>/', CaseDeviceDetail.as_view(), name='casedevice_detail'),
    path('case/<int:casepk>/device/<int:pk>/update/', CaseDeviceUpdate.as_view(), name='casedevice_update'),
    path('case/<int:casepk>/device/<int:pk>/delete/', CaseDeviceDelete.as_view(), name='casedevice_delete'),
    #path('case/<int:casepk>/device/list/', CaseDeviceList.as_view(), name='casedevice_list'),
    # Case Person
    path('case/<int:casepk>/person/', CaseEntityHome.as_view(), name='caseentity'),    
    path('case/<int:casepk>/person/create/', CasePersonCreate.as_view(), name='caseperson_create'),
    path('case/<int:casepk>/person/<int:pk>/', CasePersonDetail.as_view(), name='caseperson_detail'),
    path('case/<int:casepk>/person/<int:pk>/update/', CasePersonUpdate.as_view(), name='caseperson_update'),
    path('case/<int:casepk>/person/<int:pk>/delete/', CasePersonDelete.as_view(), name='caseperson_delete'),
    #path('case/<int:casepk>/person/list/', CasePersonList.as_view(), name='caseperson_list'),
    # Case Company
    path('case/<int:casepk>/company/', CaseEntityHome.as_view(), name='caseentity'),
    path('case/<int:casepk>/company/create/', CaseCompanyCreate.as_view(), name='casecompany_create'),
    path('case/<int:casepk>/company/<int:pk>/', CaseCompanyDetail.as_view(), name='casecompany_detail'),
    path('case/<int:casepk>/company/<int:pk>/update/', CaseCompanyUpdate.as_view(), name='casecompany_update'),
    path('case/<int:casepk>/company/<int:pk>/delete/', CaseCompanyDelete.as_view(), name='casecompany_delete'),
    #path('case/<int:casepk>/company/list/', CaseCompanyList.as_view(), name='casecompany_list'),

    # Inventory
    path('inventory/', InventoryHome.as_view(), name='devices'),
    path('inventory/create/', DeviceCreate.as_view(), name='device_create'),
    path('inventory/<int:pk>/', DeviceDetail.as_view(), name='device_detail'),
    path('inventory/<int:pk>/update/', DeviceUpdate.as_view(), name='device_update'),
    path('inventory/<int:pk>/delete/', DeviceUpdate.as_view(), name='device_delete'),

    # Loan
    path('inventory/loan/', LoanCreate.as_view(), name='loan_create'),

    # Entity
    path('entity/', EntityHome.as_view(), name='entities'),
    # Entity - Person
    path('entity/person/create/', person_add, name='person_add'),
    path('entity/person/<int:object_id>/', person_detail, name='person_detail'),
    path('entity/person/<int:object_id>/edit/', person_update, name='person_update'),
    path('entity/person/<int:object_id>/delete/', person_delete, name='person_delete'),
    #path('entity/person/<int:object_id>/export/', person_vcard_export, name="person_vcard_export"),
    #path('entity/person/search/', person_search, {'query':None},name='ab_all'),
    # Entity - Company
    path('entity/company/create/', company_add, name='company_add'),
    path('entity/company/<int:object_id>/', company_detail, name='company_detail'),
    path('entity/company/<int:object_id>/edit/', company_edit, name='company_edit'),
    path('entity/company/<int:object_id>/delete/', company_delete, name='company_delete'),
    #path('entity/company/<int:object_id>/export/', company_vcard_export, name="company_vcard_export"),
    #path('entity/company/search/', company_search, {'query':None},name='ab_all'),

    ## Note
    #path('note/<int:pk>/edit/', NoteUpdate.as_view(), name='note_edit'),
    #path('note/<int:pk>/', NoteDetail.as_view(), name='note_detail'),
    #path('note/<int:pk>/delete/', NoteDelete.as_view(), name='note_delete'),
    #path('note/create/', NoteCreate.as_view(), name='note_create'),
    ## Note Display
    #path('note/list/', NoteList.as_view(), name='note_list'),
    #path('note/table/', NoteTable.as_view(), name='note_table'),
    #path('note/', NoteHome.as_view(), name='note'),

    ## Evidence
    #path('evidence/<int:pk>/edit/', EvidenceUpdate.as_view(), name='evidence_edit'),
    #path('evidence/<int:pk>/', EvidenceDetail.as_view(), name='evidence_detail'),
    #path('evidence/<int:pk>/delete/', EvidenceDelete.as_view(), name='evidence_delete'),
    #path('evidence/create/', EvidenceCreate.as_view(), name='evidence_create'),
    ## Evidence Display
    #path('evidence/list/', EvidenceList.as_view(), name='evidence_list'),
    #path('evidence/table/', EvidenceTable.as_view(), name='evidence_table'),
    #path('evidence/', EvidenceHome.as_view(), name='evidence'),

    ## Task
    #path('task/<int:pk>/edit/', TaskUpdate.as_view(), name='task_edit'),
    #path('task/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    #path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    #path('task/create/', TaskCreate.as_view(), name='task_create'),
    ## Task Display
    #path('task/list/', TaskList.as_view(), name='task_list'),
    #path('task/table/', TaskTable.as_view(), name='task_table'),
    #path('task/', TaskHome.as_view(), name='tasks'),
    
    # Needed for Django Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    # Login
    path('login',
        django.contrib.auth.views.login,
        {
            'template_name': 'registration/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    # Logout
    path('logout',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
  
    # Uncomment the admin/doc line below to enable admin documentation:
    path('admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),

    # Base CatchAll
    url(r'^$', CaseHome.as_view(), name='home'),
]

# Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path ('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns