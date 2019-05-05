## Case Task Views ##

from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from utils.forms import BootstrapAuthenticationForm
#from case.filters import CaseFilter
from case.models import Case
from case.models import CaseTask
from case.forms.task import CaseTaskCreateForm
from case.forms.task import CaseTaskUpdateForm


## Case Task 
class CaseTaskHome(TemplateView):
    template_name = 'case/task/casetask_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseTaskHome, self).get_context_data(**kwargs)
        thiscase = Case.objects.get(pk=self.kwargs['casepk'])
        tasks = CaseTask.objects.filter(case=thiscase).filter(case__pk=self.kwargs['casepk'])
        active_tasks = CaseTask.objects.filter(case=thiscase).filter(status__title__icontains='active')
        task_history = []
        history_count = 0
        counts = {}
        updates = {}
        for task in tasks:
            task_history.append(task.history.most_recent())
            history_count += 1
        all_task_count = CaseTask.objects.filter(case=thiscase).count()
        active_task_count = CaseTask.objects.filter(case=thiscase).filter(status__title__icontains='active').count()
        # Count Dictionaries
        counts["history"] = {'name':"Task History",'value':history_count}
        counts["all"] = {'name':"All Tasks",'value':all_task_count}
        counts["active"] = {'name':"Active Tasks",'value':active_task_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"Active Tasks",
                           'object_type_plural':'Tasks',
                           'content':active_tasks,
                           'count':active_task_count}
        updates["centre"] = {'side':"centre",
                           'name':"All Tasks",
                           'object_type_plural':'Tasks',
                           'content':tasks,
                           'count':all_task_count}
        updates["right"] = {'side':"right",
                           'name':"Task History",
                           'object_type_plural':'Tasks',
                           'content':task_history,
                           'count':history_count}
        # Context
        #context['all_count'] = all_task_count
        #context['history_count'] = history_count
        #context['active_count'] = active_task_count
        context['table_objects'] = tasks
        #context['task_history'] = task_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Tasks'
        context['object'] = thiscase
        return context


class CaseTaskDetail(DetailView):
    model = CaseTask
    template_name = 'case/task/casetask_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseTaskDetail, self).get_context_data(**kwargs)
        return context


class CaseTaskCreate(CreateView):
    model = CaseTask
    template_name = 'case/task/casetask_create.html'
    form_class=CaseTaskCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseTaskCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseTaskCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseTaskUpdate(UpdateView):
    model = CaseTask
    template_name = 'case/task/casetask_update.html'
    form_class=CaseTaskUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CaseTaskUpdate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('casetask_detail', kwargs={'pk': pk, 'casepk' : casepk})


class CaseTaskList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskList, self).dispatch(request, *args, **kwargs)

    def get(self, request):
            try:
                task_ids = []
                tasks = []
                for task in CaseTask.objects.filter(case__in=self.kwargs['casepk']):
                    task_ids.append(task.pk)
                    tasks = CaseTask.objects.filter(pk__in=task_ids)
            except CaseTask.DoesNotExist:
                tasks = []
            return render(request, 'case/task/casetask_list.html', {
                'objects': tasks,
            })

    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context
