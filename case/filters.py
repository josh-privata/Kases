## Case Filters ##

import django_filters
from case.models import Case

""" Filters
BooleanFilter()
ChoiceFilter(choices=STATUS_CHOICES)
DateFilter()
ModelChoiceFilter(queryset=departments)
ModelMultipleChoiceFilter(
        field_name='attr__uuid',
        to_field_name='uuid',
        queryset=Foo.objects.all(),
    )
NumberFilter(field_name='price', lookup_expr='gt')
CharFilter(lookup_expr='icontains')
"""

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


class CaseFilter(django_filters.FilterSet):
    brief = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='icontains')
    classification = django_filters.CharFilter(lookup_expr='icontains')
    priority = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    authorisation = django_filters.CharFilter(lookup_expr='icontains')
    assigned_to = django_filters.CharFilter(lookup_expr='icontains')
    manager = django_filters.CharFilter(lookup_expr='icontains')
    assigned_by = django_filters.CharFilter(lookup_expr='icontains')
    private = django_filters.BooleanFilter()
    created = django_filters.DateFilter() 
    modified = django_filters.DateFilter() 

    class Meta:
        model = Case
        fields = ('brief', 'description', 'type', 'status', 'classification', 'priority', 'category',
                    'authorisation', 'assigned_to', 'manager', 'assigned_by', 'private', 'created', 'modified')