"""
Task Views
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from task.forms import TaskCreateForm, TaskEditForm, CrispyTaskForm
from task.models import Task
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from task.tables import TaskTable, FullTaskTable
from django_tables2 import RequestConfig, SingleTableView
from django.urls import reverse
from django.shortcuts import get_object_or_404
import base.views


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the task of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
        
# Task Main
class TaskHome(TemplateView):
    template_name = 'task/task_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(TaskHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskHome, self).get_context_data(**kwargs)
        tasks = Task.objects.all()
        context['objects1'] = tasks
        context['objects2'] = tasks
        context['objects3'] = tasks
        context['table_objects'] = tasks
        task_history = []
        history_count = 0
        for task in tasks:
            task_history.append(task.history.most_recent())
            history_count += 1
        context['task_history'] = task_history
        context['history_count'] = history_count
        context['active_count'] = Task.objects.filter(status__title__icontains='active').count()
        context['all_count'] = Task.objects.count()
        return context


class TaskDetail(DetailView):
    model = Task
    template_name_suffix = '_detail'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(TaskDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        return context


class TaskCreate(CreateView):
    model = Task
    template_name_suffix = '_create'
    form_class=CrispyTaskForm

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(TaskCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('task_detail', kwargs={'pk': self.object.pk})


class TaskUpdate(UpdateView):
    model = Task
    form_class=TaskEditForm
    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief', 'comment', 'private', 'type', 'status',
    #             'classification', 'priority', 'authorisation', 'image_upload']
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(TaskUpdate, self).dispatch(request, *args, **kwargs)


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    template_name = 'task/task_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(TaskDelete, self).dispatch(request, *args, **kwargs)


# Task Displays
class TaskTable(SingleTableView):
    model = Task
    table_class = FullTaskTable

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(TaskTable, self).dispatch(request, *args, **kwargs)


class TaskList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(TaskList, self).dispatch(request, *args, **kwargs)

    def get(self, request):
            try:
                task_ids = []
                tasks = []
                for task in Task.objects.all():
                    task_ids.append(task.pk)
                    tasks = Task.objects.filter(pk__in=task_ids)
            except Task.DoesNotExist:
                tasks = []
            return render(request, 'task/task_list.html', {
                'objects': tasks,
            })


 #Task Notes
#class TaskNoteCreate(CreateView):
#    model = TaskNote
#    template_name = 'task/note/tasknote_create.html'
#    form_class=TaskNoteCreateForm
#    task = None
    
#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            form = base.forms.BootstrapAuthenticationForm()
#            return render(request, 'registration/login.html', {'form': form})
#        else:
#            return super(TaskNoteCreate, self).dispatch(request, *args, **kwargs)

#    def get_success_url(self, **kwargs):
#        return reverse("task_detail", kwargs={'pk': self.object.pk})

#    def get(self, request, *args, **kwargs):
#        self.object = None
#        taskpk = kwargs.get('taskpk')
#        self.task = Task.objects.get(pk=taskpk)
#        context_data = self.get_context_data()
#        context_data.update(task=self.task)
#        return self.render_to_response(context_data)  

#    def get_form_kwargs(self):
#        kwargs = super(TaskNoteCreate, self).get_form_kwargs()
#        kwargs.update({'task': self.task})
#        return kwargs


#class TaskNoteUpdate(UpdateView):
#    model = TaskNote
#    form_class=TaskNoteEditForm
#    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief', 'comment', 'private', 'type', 'status',
#    #             'classification', 'priority', 'authorisation', 'image_upload']
#    template_name_suffix = 'note_update'


#class TaskNoteDelete(DeleteView):
#    model = TaskNote
#    success_url = reverse_lazy('tasknote_list')


# Task task_task.html', {'form': form})