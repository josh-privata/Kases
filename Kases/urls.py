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
from case.views.case import CaseList, CaseCreate, CaseTable, CaseDelete
from case.views.case import CaseUpdate, CaseHome, CaseDetail, case_table
#from case.views import CaseNoteUpdate, CaseNoteDetail, CaseNoteDelete
#from case.views import CaseNoteCreate, CaseNoteList, CaseNoteHome
from case.views.caseevent import CaseEventUpdate, CaseEventDetail, CaseEventDelete
from case.views.caseevent import CaseEventCreate, CaseEventList, CaseEventHome
from case.views.caseevidence import CaseEvidenceUpdate, CaseEvidenceDetail, CaseEvidenceDelete
from case.views.caseevidence import CaseEvidenceCreate, CaseEvidenceList, CaseEvidenceHome
from case.views.casetask import CaseTaskUpdate, CaseTaskDetail, CaseTaskDelete
from case.views.casetask import CaseTaskCreate, CaseTaskList, CaseTaskHome
from case.views.casedevice import CaseDeviceUpdate, CaseDeviceDetail, CaseDeviceDelete
from case.views.casedevice import CaseDeviceHome
from case.views.caseentity import CasePersonCreate, CasePersonUpdate, CaseEntityHome
from case.views.caseentity import CasePersonDetail, CasePersonDelete
from case.views.caseentity import CaseCompanyCreate, CaseCompanyUpdate
from case.views.caseentity import CaseCompanyDetail, CaseCompanyDelete
from inventory.views import InventoryHome, DeviceCreate, DeviceDetail
from inventory.views import DeviceUpdate
from loan.views import LoanHome, LoanCreate, LoanDetail, LoanUpdate, LoanDelete
from loan.views import LoanCreateWithCase, LoanCreateWithDevice
from loan.views import LoanCreateWithBoth
from loan.views import LoanUpdateWithCase, LoanUpdateWithDevice
from loan.views import LoanUpdateWithBoth
#from inventory.views import DevicesListView, HeadphonesDetail, AdapterDetail, DeviceAdd
#from inventory.views import IpadUpdate, HeadphonesUpdate, AdapterUpdate, DeviceDelete, AdapterCommentUpdate
#from inventory.views import IpadCommentDelete, IpadCommentUpdate, HeadphonesCommentDelete, HeadphonesCommentUpdate, AdapterCommentDelete
#from entity.views.company import list, detail, create, update, delete
from entity.views.person import person_delete, person_update, person_detail, person_add
from entity.views.person import PersonDetail
from entity.views.company import company_delete, company_edit, company_detail, company_add
from entity.views.entity import EntityHome
from user.views import update_profile
from utils.forms import BootstrapAuthenticationForm


admin.autodiscover()


urlpatterns = [
    ## Case ##
    path('case/', CaseHome.as_view(), name='cases'), 
    path('case/create/', CaseCreate.as_view(), name='case_create'),
    path('case/<int:pk>/', CaseDetail.as_view(), name='case_detail'),
    path('case/<int:pk>/update/', CaseUpdate.as_view(), name='case_edit'),
    path('case/<int:pk>/delete/', CaseDelete.as_view(), name='case_delete'),
    path('case/list/', CaseList.as_view(), name='case_list'),
    path('case/table/', CaseTable.as_view(), name='casetable'),
    path('case/table1/', case_table, name='case_table'),
    ## Case Events
    path('case/<int:casepk>/event/', CaseEventHome.as_view(), name='caseevent'),
    path('case/<int:casepk>/event/create/', CaseEventCreate.as_view(), name='caseevent_create'),
    path('case/<int:casepk>/event/<int:pk>/', CaseEventDetail.as_view(), name='caseevent_detail'),
    path('case/<int:casepk>/event/<int:pk>/update/', CaseEventUpdate.as_view(), name='caseevent_update'),
    path('case/<int:casepk>/event/<int:pk>/delete/', CaseEventDelete.as_view(), name='caseevent_delete'),
    path('case/<int:casepk>/event/list/', CaseEventList.as_view(), name='caseevent_list'),
    ## Case Evidence
    path('case/<int:casepk>/evidence/', CaseEvidenceHome.as_view(), name='caseevidence'),
    path('case/<int:casepk>/evidence/create/', CaseEvidenceCreate.as_view(), name='caseevidence_create'),
    path('case/<int:casepk>/evidence/<int:pk>/', CaseEvidenceDetail.as_view(), name='caseevidence_detail'),
    path('case/<int:casepk>/evidence/<int:pk>/update/', CaseEvidenceUpdate.as_view(), name='caseevidence_update'),
    path('case/<int:casepk>/evidence/<int:pk>/delete/', CaseEvidenceDelete.as_view(), name='caseevidence_delete'),
    path('case/<int:casepk>/evidence/list/', CaseEvidenceList.as_view(), name='caseevidence_list'),
    ## Case Tasks
    path('case/<int:casepk>/task/', CaseTaskHome.as_view(), name='casetask'),
    path('case/<int:casepk>/task/create/', CaseTaskCreate.as_view(), name='casetask_create'),
    path('case/<int:casepk>/task/<int:pk>/', CaseTaskDetail.as_view(), name='casetask_detail'),
    path('case/<int:casepk>/task/<int:pk>/update/', CaseTaskUpdate.as_view(), name='casetask_update'),
    path('case/<int:casepk>/task/<int:pk>/delete/', CaseTaskDelete.as_view(), name='casetask_delete'),
    path('case/<int:casepk>/task/list/', CaseTaskList.as_view(), name='casetask_list'),
    ## Case Devices
    path('case/<int:casepk>/device/', CaseDeviceHome.as_view(), name='casedevice'),
    #path('case/<int:casepk>/device/create/', CaseDeviceCreate.as_view(), name='casedevice_create'),
    path('case/<int:casepk>/device/<int:pk>/', CaseDeviceDetail.as_view(), name='casedevice_detail'),
    path('case/<int:casepk>/device/<int:pk>/update/', CaseDeviceUpdate.as_view(), name='casedevice_update'),
    path('case/<int:casepk>/device/<int:pk>/delete/', CaseDeviceDelete.as_view(), name='casedevice_delete'),
    #path('case/<int:casepk>/device/list/', CaseDeviceList.as_view(), name='casedevice_list'),
    ## Case Loans
    path('case/<int:casepk>/loan/', LoanHome.as_view(), name='loanswithcase'),
    path('case/<int:casepk>/inventory/<int:devicepk>/loan/', LoanHome.as_view(), name='loanswithboth'),
    path('case/<int:casepk>/loan/<int:pk>/', LoanDetail.as_view(), name='loanwithcase_detail'),
    path('case/<int:casepk>/inventory/<int:devicepk>/loan/<int:pk>/', LoanDetail.as_view(), name='loanwithboth_detail'),
    path('case/<int:casepk>/loan/create/', LoanCreateWithCase.as_view(), name='loanwithcase_create'),
    path('case/<int:casepk>/loan/update/', LoanUpdateWithCase.as_view(), name='loanwithcase_update'),  
    ## Case Person
    path('case/<int:casepk>/person/', CaseEntityHome.as_view(), name='caseentity'),    
    path('case/<int:casepk>/person/create/', CasePersonCreate.as_view(), name='caseperson_create'),
    path('case/<int:casepk>/person/<int:pk>/', CasePersonDetail.as_view(), name='caseperson_detail'),
    path('case/<int:casepk>/person/<int:pk>/update/', CasePersonUpdate.as_view(), name='caseperson_update'),
    path('case/<int:casepk>/person/<int:pk>/delete/', CasePersonDelete.as_view(), name='caseperson_delete'),
    #path('case/<int:casepk>/person/list/', CasePersonList.as_view(), name='caseperson_list'),
    ## Case Company
    path('case/<int:casepk>/company/', CaseEntityHome.as_view(), name='caseentity'),
    path('case/<int:casepk>/company/create/', CaseCompanyCreate.as_view(), name='casecompany_create'),
    path('case/<int:casepk>/company/<int:pk>/', CaseCompanyDetail.as_view(), name='casecompany_detail'),
    path('case/<int:casepk>/company/<int:pk>/update/', CaseCompanyUpdate.as_view(), name='casecompany_update'),
    path('case/<int:casepk>/company/<int:pk>/delete/', CaseCompanyDelete.as_view(), name='casecompany_delete'),
    #path('case/<int:casepk>/company/list/', CaseCompanyList.as_view(), name='casecompany_list'),
    
    
    ## Inventory ##
    path('inventory/', InventoryHome.as_view(), name='devices'),
    path('inventory/create/', DeviceCreate.as_view(), name='device_create'),
    path('inventory/<int:pk>/', DeviceDetail.as_view(), name='device_detail'),
    path('inventory/<int:pk>/update/', DeviceUpdate.as_view(), name='device_update'),
    path('inventory/<int:pk>/delete/', DeviceUpdate.as_view(), name='device_delete'),
    ## Loan with Inventory
    path('inventory/<int:devicepk>/loan/', LoanHome.as_view(), name='loanswithdevice'),
    path('inventory/<int:devicepk>/loan/<int:pk>/', LoanDetail.as_view(), name='loanwithdevice_detail'),    
    path('inventory/<int:devicepk>/case/<int:casepk>/loan/<int:pk>/', LoanDetail.as_view(), name='loanwithboth_detail'),
    path('inventory/<int:devicepk>/loan/create', LoanCreateWithDevice.as_view(), name='loanwithdevice_create'),
    path('inventory/<int:devicepk>/loan/<int:pk>/update', LoanUpdateWithDevice.as_view(), name='loanwithdevice_update'),
    path('inventory/<int:devicepk>/loan/<int:pk>/delete/', LoanDelete.as_view(), name='loanwithdevice_delete'),
    ## Loan
    path('loan/', LoanHome.as_view(), name='loans'),
    path('loan/<int:pk>/', LoanDetail.as_view(), name='loan_detail'),
    path('loan/create', LoanCreate.as_view(), name='loan_create'),
    path('loan/<int:pk>/update/', LoanUpdate.as_view(), name='loan_update'),    
    path('loan/<int:pk>/delete/', LoanDelete.as_view(), name='loan_delete'),
    
    ## Loan Request
    ### Return Request

    ## Entity ##
    path('entity/', EntityHome.as_view(), name='entities'),
    ## Entity - Person
    ## TODO change _add to _create   
    path('entity/person/create/', person_add, name='person_add'),
    path('entity/person/<int:pk>/', PersonDetail.as_view(), name='person_detail'),
    #path('entity/person/<int:object_id>/', person_detail, name='person_detail'),
    path('entity/person/<int:object_id>/update/', person_update, name='person_update'),
    path('entity/person/<int:object_id>/delete/', person_delete, name='person_delete'),
    #path('entity/person/<int:object_id>/export/', person_vcard_export, name="person_vcard_export"),
    #path('entity/person/search/', person_search, {'query':None},name='ab_all'),
    ## Entity - Company
    ## TODO change _add to _create
    path('entity/company/create/', company_add, name='company_add'),
    path('entity/company/<int:object_id>/', company_detail, name='company_detail'),
    path('entity/company/<int:object_id>/update/', company_edit, name='company_edit'),
    path('entity/company/<int:object_id>/delete/', company_delete, name='company_delete'),
    #path('entity/company/<int:object_id>/export/', company_vcard_export, name="company_vcard_export"),
    #path('entity/company/search/', company_search, {'query':None},name='ab_all'),


    ##User ##
    path('user/', update_profile, name='user'),

    ## Note ##
    #path('note/<int:pk>/edit/', NoteUpdate.as_view(), name='note_edit'),
    #path('note/<int:pk>/', NoteDetail.as_view(), name='note_detail'),
    #path('note/<int:pk>/delete/', NoteDelete.as_view(), name='note_delete'),
    #path('note/create/', NoteCreate.as_view(), name='note_create'),
    #path('note/list/', NoteList.as_view(), name='note_list'),
    #path('note/table/', NoteTable.as_view(), name='note_table'),
    #path('note/', NoteHome.as_view(), name='note'),

    ## Evidence ##
    #path('evidence/<int:pk>/edit/', EvidenceUpdate.as_view(), name='evidence_edit'),
    #path('evidence/<int:pk>/', EvidenceDetail.as_view(), name='evidence_detail'),
    #path('evidence/<int:pk>/delete/', EvidenceDelete.as_view(), name='evidence_delete'),
    #path('evidence/create/', EvidenceCreate.as_view(), name='evidence_create'),
    #path('evidence/list/', EvidenceList.as_view(), name='evidence_list'),
    #path('evidence/table/', EvidenceTable.as_view(), name='evidence_table'),
    #path('evidence/', EvidenceHome.as_view(), name='evidence'),

    ## Task ##
    #path('task/<int:pk>/edit/', TaskUpdate.as_view(), name='task_edit'),
    #path('task/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    #path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    #path('task/create/', TaskCreate.as_view(), name='task_create'),
    #path('task/list/', TaskList.as_view(), name='task_list'),
    #path('task/table/', TaskTable.as_view(), name='task_table'),
    #path('task/', TaskHome.as_view(), name='tasks'),
    
    
    ## Needed for Django Authentication ##
    path('accounts/', include('django.contrib.auth.urls')),
    ## Login
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
    ## Logout
    path('logout',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
  
    ## Admin ##
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    ## Base CatchAll ##
    url(r'^$', CaseHome.as_view(), name='home'),
]

# Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path ('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns