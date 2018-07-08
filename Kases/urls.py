"""
Definition of urls for Kases.
"""

from datetime import datetime
from django.conf.urls import url
from django.urls import path
import django.contrib.auth.views
import base.forms
import base.views
import case.views
import entity.views
import evidence.views
import task.views
import debug_toolbar
from evidence.views import EvidenceList, EvidenceCreate, EvidenceTable, EvidenceDelete
from evidence.views import  EvidenceUpdate, EvidenceHome, EvidenceDetail
from note.views import NoteList, NoteCreate, NoteTable, NoteDelete
from note.views import  NoteUpdate, NoteHome, NoteDetail
from task.views import TaskList, TaskCreate, TaskTable, TaskDelete
from task.views import  TaskUpdate, TaskHome, TaskDetail
from case.views import CaseList, CaseCreate, CaseTable, CaseDelete
from case.views import  CaseUpdate, CaseHome, CaseDetail
from entity.views.company import CompanyCreate, CompanyDelete, CompanyDetail, CompanyUpdate
#from entity.views.company import list, detail, create, update, delete
from entity.views import company, person, group
# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [

    # Case
    path('case/<int:pk>/edit/', CaseUpdate.as_view(), name='case_edit'),
    path('case/<int:pk>/', CaseDetail.as_view(), name='case_detail'),
    path('case/<int:pk>/delete/', CaseDelete.as_view(), name='case_delete'),
    path('case/create/', CaseCreate.as_view(), name='case_create'),

    # Case Notes
    #path('case/<int:casepk>/note/create/', CaseNoteCreate.as_view(), name='casenote_create'),
    #path('case/<int:casepk>/note/<int:notepk>/edit', CaseNoteUpdate.as_view(), name='casenote_update'),
    #path('case/<int:pk>/note/<int:pk>/detail', CaseDetail.as_view(), name='case_detail'),
    #path('case/<int:pk>/note/<int:pk>/delete', CaseDelete.as_view(), name='case_delete'),
    #path('case/<int:pk>/note/list', CaseList.as_view(), name='case_list'),

    # Case Display
    path('case/list/', CaseList.as_view(), name='case_list'),
    path('case/table/', CaseTable.as_view(), name='case_table'),
    path('case/', CaseHome.as_view(), name='cases'), 

    # Note
    path('note/<int:pk>/edit/', NoteUpdate.as_view(), name='note_edit'),
    path('note/<int:pk>/', NoteDetail.as_view(), name='note_detail'),
    path('note/<int:pk>/delete/', NoteDelete.as_view(), name='note_delete'),
    path('note/create/', NoteCreate.as_view(), name='note_create'),
    path('note/', NoteHome.as_view(), name='note'),

    # Evidence
    path('evidence/<int:pk>/edit/', EvidenceUpdate.as_view(), name='evidence_edit'),
    path('evidence/<int:pk>/', EvidenceDetail.as_view(), name='evidence_detail'),
    path('evidence/<int:pk>/delete/', EvidenceDelete.as_view(), name='evidence_delete'),
    path('evidence/create/', EvidenceCreate.as_view(), name='evidence_create'),
    path('evidence/', EvidenceHome.as_view(), name='evidence'),

    # Task
    path('task/<int:pk>/edit/', TaskUpdate.as_view(), name='task_edit'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('task/create/', TaskCreate.as_view(), name='task_create'),
    path('task/', TaskHome.as_view(), name='tasks'), 

    ## Entity
    path('companies/create/', company.create, name='company_create'),
    #path('companies/submit', CompanyFormView.as_view(), name='company'),
    path('companies/<int:pk>/', company.detail, name='company_detail'),
    path('companies/<int:pk>/delete/', company.delete, name='company_delete'),
    path('companies/<int:pk>/edit/', company.update, name='company_update'),
    path('companies/page/<int:page>/', company.list, name='company_list_paginated'),
    path('companies/', company.list, name='company_list'),

    path('people/page/<int:page>/', person.list, name='contacts_person_list_paginated'),
    path('people/add/', person.create, name='contacts_person_create'),
    path('people/<int:pk>-<slug:slug>/delete/', person.delete, name='contacts_person_delete'),
    path('people/<int:pk>/delete/', person.delete, name='contacts_person_delete'),
    path('people/<int:pk>-<slug:slug>/edit/', person.update, name='contacts_person_update'),
    path('people/<int:pk>/edit/', person.update, name='contacts_person_update'),
    path('people/<int:pk>-<slug:slug>/', person.detail, name='contacts_person_detail'),
    path('people/<int:pk>/', person.detail, name='contacts_person_detail'),
    path('people/', person.list, name='contacts_person_list'),

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
]
