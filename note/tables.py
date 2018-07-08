"""
Note Tables
"""


from note.models import Note
import django_tables2 as tables


class NoteTable(tables.Table):
    #view_entries = tables.TemplateColumn('<a href="{% url \'note_detail\' note.id %}">View</a>')

    class Meta:
        model = Note
        fields = ('id', 'title', 'reference', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Note Reference', 'Note Background', 'Note Location', 'Note Description', 'Note Brief', 'Comment', 'Note Authorisation' ,
        #                   #'Note Image Upload', 'Note Priority' )


class FullNoteTable(tables.Table):  
    view_entries = tables.TemplateColumn('<a href="{% url \'note_detail\' note.id %}">View</a>')

    class Meta:
        model = Note
        fields = ('id', 'title', 'reference', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Note Reference', 'Note Background', 'Note Location', 'Note Description', 'Note Brief', 'Comment', 'Note Authorisation' ,
        #                   #'Note Imag
