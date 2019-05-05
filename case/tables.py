# Cases Tables

from case.models import Case
import django_tables2 as tables

""" Case
'brief', 'description'
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'private'
"""

""" Case Person
'role', 'notes', 'type', 'person', 'case', 'linked_by', 'brief', 'description'
"""

""" Case Company
'role', 'notes', 'type', 'company', 'case', 'linked_by', 'brief', 'description'
"""

""" Case Device
'reason', 'description', 'expected_use', 'device', 'linked_by'
"""

""" Case Evidence
'title', 'reference', 'comment', 'bag_number', 'location',
'uri', 'current_status', 'qr_code_text', 'qr_code', 'retention_reminder_sent',
'retention_date', 'brief', 'custodian', 'chain_of_custody',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'assigned_by',
'description', 'private'
"""

""" Case Task
'title', 'background', 'location', 'brief',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'description', 'private', 'note', 'person', 'company', 'inventory',
'evidence
"""

""" Case Note
'title', 'image_upload', 'brief',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'description', 'private'
"""

""" Case Event
'title', 'image_upload', 'brief',
'type', 'status', 'classification', 'priority', 'category',
'authorisation', 'assigned_to', 'manager', 'assigned_by',
'description', 'private', 'person', 'company', 'evidence'
"""

class CaseTable(tables.Table):
    class Meta:
        model = Case
        #fields = '__all__'
        #exclude = ('Case Reference', 'Case Background', 'Case Location', 'Case Description', 'Case Brief', 'Comment', 'Case Authorisation' ,
        #                   #'Case Image Upload', 'Case Priority' )


class FullCaseTable(tables.Table):  
    #view_entries = tables.TemplateColumn('<a href="{% url \'case_detail\' case.id %}">View</a>')

    class Meta:
        model = Case
        #fields = '__all__'
        #exclude = ('Case Reference', 'Case Background', 'Case Location', 'Case Description', 'Case Brief', 'Comment', 'Case Authorisation' ,
        #                   #'Case Image Upload', 'Case Priority' )