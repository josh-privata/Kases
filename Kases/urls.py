"""
Definition of urls for Kases.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth import views
#from case.views.case import CaseList
from case.views.case import CaseCreate
from case.views.case import CaseTable
from case.views.case import CaseUpdate
from case.views.case import CaseHome
from case.views.case import CaseDetail
from case.views.case import case_table
from case.views.caseevent import CaseEventUpdate
from case.views.caseevent import CaseEventDetail
from case.views.caseevent import CaseEventCreate
from case.views.caseevent import CaseEventList
from case.views.caseevent import CaseEventHome
from case.views.caseevidence import CaseEvidenceUpdate
from case.views.caseevidence import CaseEvidenceDetail
from case.views.caseevidence import CaseEvidenceCreate
from case.views.caseevidence import CaseEvidenceList
from case.views.caseevidence import CaseEvidenceHome
from case.views.casetask import CaseTaskUpdate
from case.views.casetask import CaseTaskDetail
from case.views.casetask import CaseTaskCreate
from case.views.casetask import CaseTaskList
from case.views.casetask import CaseTaskHome
from case.views.casedevice import CaseDeviceUpdate
from case.views.casedevice import CaseDeviceDetail
from case.views.casedevice import CaseDeviceHome
from case.views.caseentity import CasePersonCreate
from case.views.caseentity import CasePersonUpdate
from case.views.caseentity import CaseEntityHome
from case.views.caseentity import CasePersonDetail
from case.views.caseentity import CaseCompanyCreate
from case.views.caseentity import CaseCompanyUpdate
from case.views.caseentity import CaseCompanyDetail
from inventory.views import InventoryHome
from inventory.views import DeviceCreate
from inventory.views import DeviceDetail
from inventory.views import DeviceUpdate
from loan.views import LoanHome
from loan.views import LoanCreate
from loan.views import LoanDetail
from loan.views import LoanUpdate
from loan.views import LoanCreateWithCase
from loan.views import LoanCreateWithDevice
from loan.views import LoanCreateWithBoth
from loan.views import LoanUpdateWithCase
from loan.views import LoanUpdateWithDevice
from loan.views import LoanUpdateWithBoth
from entity.views.person import person_update
from entity.views.person import person_detail
from entity.views.person import person_add
from entity.views.person import PersonDetail
from entity.views.company import company_edit
from entity.views.company import company_detail
from entity.views.company import company_add
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
    #path('case/list/', CaseList.as_view(), name='case_list'),
    path('case/table/', CaseTable.as_view(), name='casetable'),
    #path('case/table1/', case_table, name='case_table'),
    ## Case Events
    path('case/<int:casepk>/event/', CaseEventHome.as_view(), name='caseevent'),
    path('case/<int:casepk>/event/create/', CaseEventCreate.as_view(), name='caseevent_create'),
    path('case/<int:casepk>/event/<int:pk>/', CaseEventDetail.as_view(), name='caseevent_detail'),
    path('case/<int:casepk>/event/<int:pk>/update/', CaseEventUpdate.as_view(), name='caseevent_update'),
    path('case/<int:casepk>/event/list/', CaseEventList.as_view(), name='caseevent_list'),
    ## Case Evidence
    path('case/<int:casepk>/evidence/', CaseEvidenceHome.as_view(), name='caseevidence'),
    path('case/<int:casepk>/evidence/create/', CaseEvidenceCreate.as_view(), name='caseevidence_create'),
    path('case/<int:casepk>/evidence/<int:pk>/', CaseEvidenceDetail.as_view(), name='caseevidence_detail'),
    path('case/<int:casepk>/evidence/<int:pk>/update/', CaseEvidenceUpdate.as_view(), name='caseevidence_update'),
    path('case/<int:casepk>/evidence/list/', CaseEvidenceList.as_view(), name='caseevidence_list'),
    ## Case Tasks
    path('case/<int:casepk>/task/', CaseTaskHome.as_view(), name='casetask'),
    path('case/<int:casepk>/task/create/', CaseTaskCreate.as_view(), name='casetask_create'),
    path('case/<int:casepk>/task/<int:pk>/', CaseTaskDetail.as_view(), name='casetask_detail'),
    path('case/<int:casepk>/task/<int:pk>/update/', CaseTaskUpdate.as_view(), name='casetask_update'),
    path('case/<int:casepk>/task/list/', CaseTaskList.as_view(), name='casetask_list'),
    ## Case Devices
    path('case/<int:casepk>/device/', CaseDeviceHome.as_view(), name='casedevice'),
    path('case/<int:casepk>/device/<int:pk>/', CaseDeviceDetail.as_view(), name='casedevice_detail'),
    path('case/<int:casepk>/device/<int:pk>/update/', CaseDeviceUpdate.as_view(), name='casedevice_update'),
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
    ## Case Company
    path('case/<int:casepk>/company/', CaseEntityHome.as_view(), name='caseentity'),
    path('case/<int:casepk>/company/create/', CaseCompanyCreate.as_view(), name='casecompany_create'),
    path('case/<int:casepk>/company/<int:pk>/', CaseCompanyDetail.as_view(), name='casecompany_detail'),
    path('case/<int:casepk>/company/<int:pk>/update/', CaseCompanyUpdate.as_view(), name='casecompany_update'),
    
    ## Inventory ##
    path('inventory/', InventoryHome.as_view(), name='devices'),
    path('inventory/create/', DeviceCreate.as_view(), name='device_create'),
    path('inventory/<int:pk>/', DeviceDetail.as_view(), name='device_detail'),
    path('inventory/<int:pk>/update/', DeviceUpdate.as_view(), name='device_update'),
    ## Loan with Inventory
    path('inventory/<int:devicepk>/loan/', LoanHome.as_view(), name='loanswithdevice'),
    path('inventory/<int:devicepk>/loan/<int:pk>/', LoanDetail.as_view(), name='loanwithdevice_detail'),    
    path('inventory/<int:devicepk>/case/<int:casepk>/loan/<int:pk>/', LoanDetail.as_view(), name='loanwithboth_detail'),
    path('inventory/<int:devicepk>/loan/create', LoanCreateWithDevice.as_view(), name='loanwithdevice_create'),
    path('inventory/<int:devicepk>/loan/<int:pk>/update', LoanUpdateWithDevice.as_view(), name='loanwithdevice_update'),
    ## Loan
    path('loan/', LoanHome.as_view(), name='loans'),
    path('loan/<int:pk>/', LoanDetail.as_view(), name='loan_detail'),    
    ## Loan Request
    path('loan/create', LoanCreate.as_view(), name='loan_create'),
    path('loan/<int:pk>/update/', LoanUpdate.as_view(), name='loan_update'),    
    ### Return Request

    ## Entity ##
    path('entity/', EntityHome.as_view(), name='entities'),
    ## Entity - Person
    ## TODO change _add to _create   
    path('entity/person/create/', person_add, name='person_add'),
    path('entity/person/<int:pk>/', PersonDetail.as_view(), name='person_detail'),
    path('entity/person/<int:object_id>/update/', person_update, name='person_update'),
    #path('entity/person/<int:object_id>/export/', person_vcard_export, name="person_vcard_export"),
    #path('entity/person/search/', person_search, {'query':None},name='ab_all'),
    ## Entity - Company
    ## TODO change _add to _create
    path('entity/company/create/', company_add, name='company_add'),
    path('entity/company/<int:object_id>/', company_detail, name='company_detail'),
    path('entity/company/<int:object_id>/update/', company_edit, name='company_edit'),
    #path('entity/company/<int:object_id>/export/', company_vcard_export, name="company_vcard_export"),
    #path('entity/company/search/', company_search, {'query':None},name='ab_all'),

    ## User ##
    path('user/', update_profile, name='user'),
    
    ## Needed for Django Authentication ##
    path('accounts/', include('django.contrib.auth.urls')),
    ## Login
    path('login',
        views.login,
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
        views.logout,
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