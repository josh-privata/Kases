# Cases Tables

from case.models import Case
import django_tables2 as tables


class CaseTable(tables.Table):
    #view_entries = tables.TemplateColumn('<a href="{% url \'case_detail\' case.id %}">View</a>')

    class Meta:
        model = Case
        #fields = ('id', 'title', 'reference', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Case Reference', 'Case Background', 'Case Location', 'Case Description', 'Case Brief', 'Comment', 'Case Authorisation' ,
        #                   #'Case Image Upload', 'Case Priority' )


class FullCaseTable(tables.Table):  
    #view_entries = tables.TemplateColumn('<a href="{% url \'case_detail\' case.id %}">View</a>')

    class Meta:
        model = Case
        fields = '__all__'
        #exclude = ('Case Reference', 'Case Background', 'Case Location', 'Case Description', 'Case Brief', 'Comment', 'Case Authorisation' ,
        #                   #'Case Image Upload', 'Case Priority' )