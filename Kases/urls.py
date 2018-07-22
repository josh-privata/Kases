"""
Definition of urls for Kases.
"""

from datetime import datetime
from django.conf.urls import url
from django.urls import path
import django.contrib.auth.views
from django.conf.urls import include
from django.contrib import admin
import base.forms
import base.views
#from evidence.views import EvidenceList, EvidenceCreate, EvidenceTable, EvidenceDelete
#from evidence.views import EvidenceUpdate, EvidenceHome, EvidenceDetail
#from note.views import NoteList, NoteCreate, NoteTable, NoteDelete
#from note.views import  NoteUpdate, NoteHome, NoteDetail
#from task.views import TaskList, TaskCreate, TaskTable, TaskDelete
#from task.views import TaskUpdate, TaskHome, TaskDetail
from case.views import CaseList, CaseCreate, CaseTable, CaseDelete
from case.views import CaseUpdate, CaseHome, CaseDetail
from case.views import CaseNoteUpdate, CaseNoteDetail, CaseNoteDelete
from case.views import CaseNoteCreate, CaseNoteList
from case.views import CaseEvidenceUpdate, CaseEvidenceDetail, CaseEvidenceDelete
from case.views import CaseEvidenceCreate, CaseEvidenceList
from case.views import CaseTaskUpdate, CaseTaskDetail, CaseTaskDelete
from case.views import CaseTaskCreate, CaseTaskList
#from asset.views import DevicesListView, AssetHome, IpadDetail, HeadphonesDetail, AdapterDetail, DeviceAdd
#from asset.views import IpadUpdate, HeadphonesUpdate, AdapterUpdate, DeviceDelete, AdapterCommentUpdate
#from asset.views import IpadCommentDelete, IpadCommentUpdate, HeadphonesCommentDelete, HeadphonesCommentUpdate, AdapterCommentDelete
#from entity.views.company import list, detail, create, update, delete
from entity.views import company, person, group


admin.autodiscover()


urlpatterns = [

    # Case
    path('case/<int:pk>/update/', CaseUpdate.as_view(), name='case_edit'),
    path('case/<int:pk>/', CaseDetail.as_view(), name='case_detail'),
    path('case/<int:pk>/delete/', CaseDelete.as_view(), name='case_delete'),
    path('case/create/', CaseCreate.as_view(), name='case_create'),
    # Case Display
    path('case/list/', CaseList.as_view(), name='case_list'),
    path('case/table/', CaseTable.as_view(), name='case_table'),
    # Case Notes
    path('case/<int:casepk>/note/create/', CaseNoteCreate.as_view(), name='casenote_create'),
    path('case/<int:casepk>/note/<int:pk>/update', CaseNoteUpdate.as_view(), name='casenote_update'),
    path('case/<int:casepk>/note/<int:pk>/detail', CaseNoteDetail.as_view(), name='casenote_detail'),
    path('case/<int:casepk>/note/<int:pk>/delete', CaseNoteDelete.as_view(), name='casenote_delete'),
    path('case/<int:casepk>/note/list', CaseNoteList.as_view(), name='casenote_list'),
    # Case Evidence
    path('case/<int:casepk>/evidence/create/', CaseEvidenceCreate.as_view(), name='caseevidence_create'),
    path('case/<int:casepk>/evidence/<int:pk>/update', CaseEvidenceUpdate.as_view(), name='caseevidence_update'),
    path('case/<int:casepk>/evidence/<int:pk>/detail', CaseEvidenceDetail.as_view(), name='caseevidence_detail'),
    path('case/<int:casepk>/evidence/<int:pk>/delete', CaseEvidenceDelete.as_view(), name='caseevidence_delete'),
    path('case/<int:casepk>/evidence/list', CaseEvidenceList.as_view(), name='caseevidence_list'),
    # Case Tasks
    path('case/<int:casepk>/task/create/', CaseTaskCreate.as_view(), name='casetask_create'),
    path('case/<int:casepk>/task/<int:pk>/update', CaseTaskUpdate.as_view(), name='casetask_update'),
    path('case/<int:casepk>/task/<int:pk>/detail', CaseTaskDetail.as_view(), name='casetask_detail'),
    path('case/<int:casepk>/task/<int:pk>/delete', CaseTaskDelete.as_view(), name='casetask_delete'),
    path('case/<int:casepk>/task/list', CaseTaskList.as_view(), name='casetask_list'),
    # Case CatchAll
    path('case/', CaseHome.as_view(), name='cases'), 

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

    # Company
    path('companies/create/', company.create, name='company_create'),
    #path('companies/submit', CompanyFormView.as_view(), name='company'),
    path('companies/<int:pk>/', company.detail, name='company_detail'),
    path('companies/<int:pk>/delete/', company.delete, name='company_delete'),
    path('companies/<int:pk>/edit/', company.update, name='company_update'),
    path('companies/page/<int:page>/', company.list, name='company_list_paginated'),
    path('companies/', company.list, name='company_list'),
    # People
    path('people/page/<int:page>/', person.list, name='contacts_person_list_paginated'),
    path('people/add/', person.create, name='contacts_person_create'),
    path('people/<int:pk>-<slug:slug>/delete/', person.delete, name='contacts_person_delete'),
    path('people/<int:pk>/delete/', person.delete, name='contacts_person_delete'),
    path('people/<int:pk>-<slug:slug>/edit/', person.update, name='contacts_person_update'),
    path('people/<int:pk>/edit/', person.update, name='contacts_person_update'),
    path('people/<int:pk>-<slug:slug>/', person.detail, name='contacts_person_detail'),
    path('people/<int:pk>/', person.detail, name='contacts_person_detail'),
    path('people/', person.list, name='contacts_person_list'),
    # Groups
    path('groups/page/<int:page>/', group.list, name='contacts_group_list_paginated'),
    path('groups/add/', group.create, name='contacts_group_create'),
    path('groups/<int:pk>-<slug:slug>/delete/', group.delete, name='contacts_group_delete'),
    path('groups/<int:pk>/delete/', group.delete, name='contacts_group_delete'),
    path('groups/<int:pk>-<slug:slug>/edit/', group.update, name='contacts_group_update'),
    path('groups/<int:pk>/edit/', group.update, name='contacts_group_update'),
    path('groups/<int:pk>-<slug:slug>/', group.detail, name='contacts_group_detail'),
    path('groups/<int:pk>/', group.detail, name='contacts_group_detail'),
    path('groups/', group.list, name='contacts_group_list'),
    
    # Debug Toolbar
    #path('__debug__/', include(debug_toolbar.urls)),
    
    # Needed for Django Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    # Login
    path('login',
        django.contrib.auth.views.login,
        {
            'template_name': 'registration/login.html',
            'authentication_form': base.forms.BootstrapAuthenticationForm,
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
    path('admin/doc', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('admin', admin.site.urls),

    # Base CatchAll
    url(r'^$', CaseHome.as_view(), name='home'),

    ### Assets
    #path('assets/', AssetHome.as_view(), name='index'),
    ### TODO: use just one urlpattern for all device list views
    #path('assets/ipads/', DevicesListView.as_view(), kwargs={'device_type': 'ipads'}, name='ipads'),
    #path('assets/headphones/', DevicesListView.as_view(), kwargs={'device_type': 'headphones'}, name='headphones'),
    #path('assets/adapters/', DevicesListView.as_view(), kwargs={'device_type': 'adapters'}, name='adapters'),
    ##path('assets/cases/', DevicesListView.as_view(), kwargs={'device_type': 'cases'}, name='cases'),
    #path('assets/ipads/<int:pk>/', IpadDetail.as_view(), name='ipad_detail'),
    #path('assets/headphones/<int:pk>/', HeadphonesDetail.as_view(), name='headphones_detail'),
    #path('assets/adapters/<int:pk>/', AdapterDetail.as_view(), name='adapter_detail'),
    ##path('assets/cases/<int:pk>/', CaseDetail.as_view(), name='case_detail'),
    ### Create Views
    #path('assets/add/', DeviceAdd.as_view(), name='add'),
    ### Edit Views
    #path('assets/ipads/<int:pk>/edit/', IpadUpdate.as_view(), name='ipad_update'),
    #path('assets/headphones/<int:pk>/edit/', HeadphonesUpdate.as_view(), name='headphones_update'),
    ##path('assets/cases/<int:pk>/edit/', CaseUpdate.as_view(), name='case_update'),
    #path('assets/adapters/<int:pk>/edit/', AdapterUpdate.as_view(), name='adapter_update'),
    ### Delete Views
    ##path('permissions/denied/$', TemplateView.as_view(template_name='403.html'), name='permission_denied'),
    #path('assets/<int:pk>/delete/', DeviceDelete.as_view(), name='delete'),
    ### Comments
    ### /devices/comments/12/cases/3/edit/
    #path('assets/<int:comment_id>/ipads/<int:device_id>/delete/', IpadCommentDelete.as_view(), name='ipad_delete'),
    #path('assets/<int:comment_id>/ipads/<int:device_id>/edit/', IpadCommentUpdate.as_view(), name='ipad_edit'),
    #path('assets/<int:comment_id>/headphones/<int:device_id>/delete/', HeadphonesCommentDelete.as_view(), name='headphones_delete'),
    #path('assets/<int:comment_id>/headphones/<int:device_id>/edit/', HeadphonesCommentUpdate.as_view(), name='headphones_edit'),
    #path('assets/<int:comment_id>/adapters/<int:device_id>/delete/', AdapterCommentDelete.as_view(), name='adapter_delete'),
    #path('assets/<int:comment_id>/adapters/<int:device_id>/edit/', AdapterCommentUpdate.as_view(), name='adapter_edit'),
    ##path('assets/<int:comment_id>/cases/(int:device_id>/delete/', CaseCommentDelete.as_view(), name='case_delete'),
    ##path('assets/<int:comment_id>/cases/<int:device_id>/edit/', CaseCommentUpdate.as_view(), name='case_edit'),
]
