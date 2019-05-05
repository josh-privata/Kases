# Evidence Tables

from evidence.models import Evidence
import django_tables2 as tables


class EvidenceTable(tables.Table):
    #view_entries = tables.TemplateColumn('<a href="{% url \'evidence_detail\' evidence.id %}">View</a>')

    class Meta:
        model = Evidence
        fields = ('id', 'title', 'reference', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Evidence Reference', 'Evidence Background', 'Evidence Location', 'Evidence Description', 'Evidence Brief', 'Comment', 'Evidence Authorisation' ,
        #                   #'Evidence Image Upload', 'Evidence Priority' )


class FullEvidenceTable(tables.Table):  
    view_entries = tables.TemplateColumn('<a href="{% url \'evidence_detail\' evidence.id %}">View</a>')

    class Meta:
        model = Evidence
        fields = ('id', 'title', 'reference', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Evidence Reference', 'Evidence Background', 'Evidence Location', 'Evidence Description', 'Evidence Brief', 'Comment', 'Evidence Authorisation' ,
        #                   #'Evidence Imag
