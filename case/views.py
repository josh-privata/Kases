## Case Views ##


from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from case.forms import CaseCreateForm, CaseUpdateForm, CrispyCaseForm
from case.forms import CrispyCaseNoteCreateForm, CaseNoteUpdateForm, CaseNoteCreateForm
from case.forms import CrispyCaseTaskCreateForm, CaseTaskUpdateForm, CaseTaskCreateForm
from case.forms import CrispyCaseEvidenceCreateForm, CaseEvidenceUpdateForm, CaseEvidenceCreateForm
from case.models import Case, CaseNote, CaseTask, CaseEvidence
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from case.tables import CaseTable, FullCaseTable
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
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
        

# Case Main
class CaseHome(TemplateView):
    template_name = 'case/case_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseHome, self).get_context_data(**kwargs)
        cases = Case.objects.all()
        case_history = []
        history_count = 0
        for case in cases:
            case_history.append(case.history.most_recent())
            history_count += 1
        context['objects1'] = cases
        context['objects2'] = cases
        context['objects3'] = cases
        context['table_objects'] = cases
        context['case_history'] = case_history
        context['history_count'] = history_count
        context['active_count'] = Case.objects.filter(status__title__icontains='active').count()
        context['all_count'] = Case.objects.count()
        return context


class CaseDetail(DetailView):
    model = Case
    template_name_suffix = '_detail'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseDetail, self).get_context_data(**kwargs)
        context['notes'] = CaseNote.objects.filter(case=self.object.pk)
        context['evidence'] = CaseEvidence.objects.filter(case=self.object.pk)
        context['tasks'] = CaseTask.objects.filter(case=self.object.pk)
        return context


    
class CaseCreate(CreateView):
    model = Case
    template_name_suffix = '_create'
    form_class=CrispyCaseForm

    def get_context_data(self, **kwargs):
        context = super(CaseCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('case_detail', kwargs={'pk': self.object.pk})


class CaseUpdate(UpdateView):
    model = Case
    form_class=CaseUpdateForm
    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief', 'comment', 'private', 'type', 'status',
    #             'classification', 'priority', 'authorisation', 'image_upload']
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(CaseUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseUpdate, self).dispatch(request, *args, **kwargs)


class CaseDelete(DeleteView):
    model = Case
    success_url = reverse_lazy('case_list')
    template_name = 'case/case_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDelete, self).dispatch(request, *args, **kwargs)


# Case Displays
class CaseTable(SingleTableView):
    model = Case
    table_class = CaseTable

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTable, self).dispatch(request, *args, **kwargs)


class CaseList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseList, self).dispatch(request, *args, **kwargs)

    def get(self, request):
            try:
                case_ids = []
                cases = []
                for case in Case.objects.all():
                    case_ids.append(case.pk)
                    cases = Case.objects.filter(pk__in=case_ids)
            except Case.DoesNotExist:
                cases = []
            return render(request, 'case/case_list.html', {
                'objects': cases,
            })


#Case Notes Main
class CaseNoteHome(TemplateView):
    template_name = 'case/note/casenote_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseNoteHome, self).get_context_data(**kwargs)
        case = Case.objects.get(pk=self.kwargs['casepk'])
        note_history = []
        history_count = 0
        for note in case:
            note_history.append(note.history.most_recent())
            history_count += 1
        context['objects1'] = case
        context['objects2'] = case
        context['objects3'] = case
        context['table_objects'] = case
        context['case_history'] = case_history
        context['history_count'] = history_count
        context['active_count'] = Case.objects.filter(status__title__icontains='active').count()
        context['all_count'] = CaseNot
        return context


class CaseNoteDetail(DetailView):
    model = CaseNote
    template_name = 'case/note/casenote_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseNoteDetail, self).get_context_data(**kwargs)
        return context


class CaseNoteCreate(CreateView):
    model = CaseNote
    template_name = 'case/note/casenote_create.html'
    form_class=CrispyCaseNoteCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseNoteCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})


class CaseNoteUpdate(UpdateView):
    model = CaseNote
    template_name = 'case/note/casenote_update.html'
    form_class=CaseNoteUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CaseNoteUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('casenote_detail', kwargs={'pk': pk, 'casepk' : casepk})


class CaseNoteDelete(DeleteView):
    model = CaseNote
    template_name = 'case/note/casenote_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})


#Case Notes Displays
class CaseNoteList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteList, self).dispatch(request, *args, **kwargs)

    def get(self, request):
            try:
                note_ids = []
                notes = []
                for note in CaseNote.objects.filter(case__in=self.kwargs['casepk']):
                    note_ids.append(note.pk)
                    notes = CaseNote.objects.filter(pk__in=note_ids)
            except CaseNote.DoesNotExist:
                notes = []
            return render(request, 'case/note/casenote_list.html', {
                'objects': notes,
            })


#Case Tasks Main
class CaseTaskHome(TemplateView):
    template_name = 'case/task/casetask_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseTaskHome, self).get_context_data(**kwargs)
        case = Case.objects.get(pk=self.kwargs['casepk'])
        task_history = []
        history_count = 0
        for task in case:
            task_history.append(task.history.most_recent())
            history_count += 1
        context['objects1'] = case
        context['objects2'] = case
        context['objects3'] = case
        context['table_objects'] = case
        context['case_history'] = case_history
        context['history_count'] = history_count
        context['active_count'] = Case.objects.filter(status__title__icontains='active').count()
        context['all_count'] = CaseNot
        return context


class CaseTaskDetail(DetailView):
    model = CaseTask
    template_name = 'case/task/casetask_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseTaskDetail, self).get_context_data(**kwargs)
        return context


class CaseTaskCreate(CreateView):
    model = CaseTask
    template_name = 'case/task/casetask_create.html'
    form_class=CrispyCaseTaskCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseTaskCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})


class CaseTaskUpdate(UpdateView):
    model = CaseTask
    template_name = 'case/task/casetask_update.html'
    form_class=CaseTaskUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CaseTaskUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('casetask_detail', kwargs={'pk': pk, 'casepk' : casepk})


class CaseTaskDelete(DeleteView):
    model = CaseTask
    template_name = 'case/task/casetask_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})


#Case Tasks Displays
class CaseTaskList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
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


#Case Evidences Main
class CaseEvidenceHome(TemplateView):
    template_name = 'case/evidence/caseevidence_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceHome, self).get_context_data(**kwargs)
        case = Case.objects.get(pk=self.kwargs['casepk'])
        evidence_history = []
        history_count = 0
        for evidence in case:
            evidence_history.append(evidence.history.most_recent())
            history_count += 1
        context['objects1'] = case
        context['objects2'] = case
        context['objects3'] = case
        context['table_objects'] = case
        context['case_history'] = case_history
        context['history_count'] = history_count
        context['active_count'] = Case.objects.filter(status__title__icontains='active').count()
        context['all_count'] = CaseNot
        return context


class CaseEvidenceDetail(DetailView):
    model = CaseEvidence
    template_name = 'case/evidence/caseevidence_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceDetail, self).get_context_data(**kwargs)
        return context


class CaseEvidenceCreate(CreateView):
    model = CaseEvidence
    template_name = 'case/evidence/caseevidence_create.html'
    form_class=CrispyCaseEvidenceCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseEvidenceCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})


class CaseEvidenceUpdate(UpdateView):
    model = CaseEvidence
    template_name = 'case/evidence/caseevidence_update.html'
    form_class=CaseEvidenceUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('caseevidence_detail', kwargs={'pk': pk, 'casepk' : casepk})


class CaseEvidenceDelete(DeleteView):
    model = CaseEvidence
    template_name = 'case/evidence/caseevidence_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})


#Case Evidences Displays
class CaseEvidenceList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceList, self).dispatch(request, *args, **kwargs)

    def get(self, request):
            try:
                evidence_ids = []
                evidences = []
                for evidence in CaseEvidence.objects.filter(case__in=self.kwargs['casepk']):
                    evidence_ids.append(evidence.pk)
                    evidences = CaseEvidence.objects.filter(pk__in=evidence_ids)
            except CaseEvidence.DoesNotExist:
                evidences = []
            return render(request, 'case/evidence/caseevidence_list.html', {
                'objects': evidences,
            })