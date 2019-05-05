"""
Event Tables
"""


from event.models import Event
import django_tables2 as tables


class EventTable(tables.Table):
    #view_entries = tables.TemplateColumn('<a href="{% url \'event_detail\' event.id %}">View</a>')

    class Meta:
        model = Event
        fields = ('id', 'title', 'reference', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Event Reference', 'Event Background', 'Event Location', 'Event Description', 'Event Brief', 'Comment', 'Event Authorisation' ,
        #                   #'Event Image Upload', 'Event Priority' )


class FullEventTable(tables.Table):  
    view_entries = tables.TemplateColumn('<a href="{% url \'event_detail\' event.id %}">View</a>')

    class Meta:
        model = Event
        fields = ('id', 'title', 'reference', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Event Reference', 'Event Background', 'Event Location', 'Event Description', 'Event Brief', 'Comment', 'Event Authorisation' ,
        #                   #'Event Imag
