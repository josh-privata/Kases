# Task Tables

from task.models import Task
import django_tables2 as tables


class TaskTable(tables.Table):
    #view_entries = tables.TemplateColumn('<a href="{% url \'task_detail\' task.id %}">View</a>')

    class Meta:
        model = Task
        fields = ('id', 'title', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Task Reference', 'Task Background', 'Task Location', 'Task Description', 'Task Brief', 'Comment', 'Task Authorisation' ,
        #                   #'Task Image Upload', 'Task Priority' )


class FullTaskTable(tables.Table):  
    view_entries = tables.TemplateColumn('<a href="{% url \'task_detail\' task.id %}">View</a>')



    class Meta:
        model = Task
        fields = ('id', 'title', 'private', 'creation_date', 'deadline', 'status',)
        #exclude = ('Task Reference', 'Task Background', 'Task Location', 'Task Description', 'Task Brief', 'Comment', 'Task Authorisation' ,
        #                   #'Task Imag