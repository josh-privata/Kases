## Case Views ##

from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django_tables2 import SingleTableView, RequestConfig
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
#from case.filters import CaseFilter
from case.forms import CaseUpdateForm, CrispyCaseForm, CrispyCaseUpdateForm
from case.forms import CrispyCaseNoteCreateForm, CrispyCaseNoteUpdateForm
from case.forms import CrispyCaseTaskCreateForm, CrispyCaseTaskUpdateForm
from case.forms import CrispyCaseEventCreateForm, CrispyCaseEventUpdateForm, CaseEventCreateForm, CaseEventUpdateForm, EventPersonFormset
from case.forms import CrispyCaseEvidenceCreateForm, CrispyCaseEvidenceUpdateForm
from case.forms import CaseCompanyCreateForm, CaseCompanyUpdateForm
from case.forms import CrispyCaseCompanyCreateForm, CrispyCaseCompanyUpdateForm
from case.forms import CasePersonCreateForm, CasePersonUpdateForm
from case.forms import CrispyCasePersonCreateForm, CrispyCasePersonUpdateForm
from case.forms import CaseDeviceCreateForm, CaseDeviceUpdateForm
from case.forms import CrispyCaseDeviceCreateForm, CrispyCaseDeviceUpdateForm
from case.models import Case, CaseNote, CaseTask, CaseEvidence, CasePerson, CaseCompany, CaseInventory, CaseEvent
from entity.models.person import Person
from case.tables import CaseTable
from utils.forms import BootstrapAuthenticationForm

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
        

## Case 
class CaseHome(TemplateView):
    template_name = 'case/case_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseHome, self).get_context_data(**kwargs)
        cases = Case.objects.all()
        active_cases = Case.objects.filter(status__title__icontains='active')
        case_history = []
        history_count = 0
        counts = {}
        updates = {}
        for case in cases:
            case_history.append(case.history.most_recent())
            history_count += 1
        all_case_count = Case.objects.count()
        active_case_count = Case.objects.filter(status__title__icontains='active').count()
        # Count Dictionaries
        counts["history"] = {'name':"Case History",'value':history_count}
        counts["all"] = {'name':"All Cases",'value':all_case_count}
        counts["active"] = {'name':"Active Cases",'value':active_case_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"Active Cases",
                           'object_type_plural':'Cases',
                           'content':active_cases,
                           'count':active_case_count}
        updates["centre"] = {'side':"centre",
                           'name':"All Cases",
                           'object_type_plural':'Cases',
                           'content':cases,
                           'count':all_case_count}
        updates["right"] = {'side':"right",
                           'name':"Case History",
                           'object_type_plural':'Cases',
                           'content':case_history,
                           'count':history_count}
        # Context
        #context['all_count'] = all_case_count
        #context['history_count'] = history_count
        #context['active_count'] = active_case_count
        context['table_objects'] = cases
        #context['case_history'] = case_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Cases'
        return context


class CaseTable(SingleTableView):
    model = Case
    table_class = CaseTable

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTable, self).dispatch(request, *args, **kwargs)


class CaseDetail(DetailView):
    model = Case
    template_name = 'case/case/case_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseDetail, self).get_context_data(**kwargs)
        context['notes'] = CaseNote.objects.filter(case=self.object.pk)
        context['events'] = CaseEvent.objects.filter(case=self.object.pk)
        context['evidence'] = CaseEvidence.objects.filter(case=self.object.pk)
        context['tasks'] = CaseTask.objects.filter(case=self.object.pk)
        context['persons'] = CasePerson.objects.filter(case=self.object.pk)
        context['companies'] = CaseCompany.objects.filter(case=self.object.pk)
        context['devices'] = CaseInventory.objects.filter(case=self.object.pk)
        
        #notes = CaseNote.objects.filter(case=self.object.pk)
        #events = CaseEvent.objects.filter(case=self.object.pk)
        #evidence = CaseEvidence.objects.filter(case=self.object.pk)
        #tasks = CaseTask.objects.filter(case=self.object.pk)
        #persons = CasePerson.objects.filter(case=self.object.pk)
        #companies = CaseCompany.objects.filter(case=self.object.pk)
        #devices = CaseInventory.objects.filter(case=self.object.pk)
        #updates = {}
        #updates["Notes"] = {'section':"Notes",
        #                   'url_root':"note",
        #                   'headers':('Title', 'Detail', 'Location', 'Status', 'Type'),
        #                   'fields':('title', 'detail', 'location', 'status', 'type'),
        #                   'content':notes,
        #                   'count':notes.count()}
        #updates["Event"] = {'section':"Event",
        #                   'url_root':"event",
        #                   'headers':('Title', 'Detail', 'Location', 'Status', 'Type'),
        #                   'fields':('title', 'detail', 'location', 'status', 'type'),
        #                   'content':events,
        #                   'count':events.count()}
        #updates["Evidence"] = {'section':"Evidence",
        #                   'url_root':"evidence",
        #                   'headers':('Title', 'Detail', 'Location', 'Status', 'Type'),
        #                   'fields':('title', 'detail', 'location', 'status', 'type'),
        #                   'content':evidence,
        #                   'count':evidence.count()}
        #updates["Tasks"] = {'section':"Tasks",
        #                   'url_root':"task",
        #                   'headers':('Title', 'Detail', 'Location', 'Status', 'Type'),
        #                   'fields':('title', 'detail', 'location', 'status', 'type'),
        #                   'content':tasks,
        #                   'count':tasks.count()}
        #updates["Persons"] = {'section':"Persons",
        #                   'url_root':"person",
        #                   'headers':('Title', 'Detail', 'Location', 'Status', 'Type'),
        #                   'fields':('title', 'detail', 'location', 'status', 'type'),
        #                   'content':persons,
        #                   'count':persons.count()}
        #updates["Companies"] = {'section':"Companies",
        #                   'url_root':"company",
        #                   'headers':('Title', 'Detail', 'Location', 'Status', 'Type'),
        #                   'fields':('title', 'detail', 'location', 'status', 'type'),
        #                   'content':companies,
        #                   'count':companies.count()}
        #updates["Devices"] = {'section':"Devices",
        #                   'url_root':"device",
        #                   'headers':('Title', 'Detail', 'Location', 'Status', 'Type'),
        #                   'fields':('title', 'detail', 'location', 'status', 'type'),
        #                   'content':devices,
        #                   'count':devices.count()}
        #context['updates'] = updates
        return context

    
class CaseCreate(CreateView):
    model = Case
    template_name = 'case/case/case_create.html'
    form_class=CrispyCaseForm

    def get_context_data(self, **kwargs):
        context = super(CaseCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('case_detail', kwargs={'pk': self.object.pk})


class CaseUpdate(UpdateView):
    model = Case
    form_class = CrispyCaseUpdateForm
    template_name = 'case/case/case_update.html'

    def get_context_data(self, **kwargs):
        context = super(CaseUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseUpdate, self).dispatch(request, *args, **kwargs)


class CaseDelete(DeleteView):
    model = Case
    success_url = reverse_lazy('cases')
    template_name = 'case/case/case_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDelete, self).dispatch(request, *args, **kwargs)


#def case_list(request):
#    filter = CaseFilter(request.GET, queryset=Case.objects.all())
#    return render(request, 'case/case_filter.html', {'filter': filter})


class CaseList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
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


def case_table(request):
        table = Case.objects.all()
        #RequestConfig(request).configure(table)
        return render(request, 'case/case_table.html', { 'table' : table })


## Case Note 
class CaseNoteHome(TemplateView):
    template_name = 'case/note/casenote_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseNoteHome, self).get_context_data(**kwargs)
        notes = CaseNote.objects.all()
        active_notes = CaseNote.objects.filter(status__title__icontains='active')
        note_history = []
        history_count = 0
        counts = {}
        updates = {}
        for note in notes:
            note_history.append(note.history.most_recent())
            history_count += 1
        all_note_count = CaseNote.objects.count()
        active_note_count = CaseNote.objects.filter(status__title__icontains='active').count()
        # Count Dictionaries
        counts["history"] = {'name':"Note History",'value':history_count}
        counts["all"] = {'name':"All Notes",'value':all_note_count}
        counts["active"] = {'name':"Active Notes",'value':active_note_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"Active Notes",
                           'object_type_plural':'Notes',
                           'content':active_notes,
                           'count':active_note_count}
        updates["centre"] = {'side':"centre",
                           'name':"All Notes",
                           'object_type_plural':'Notes',
                           'content':notes,
                           'count':all_note_count}
        updates["right"] = {'side':"right",
                           'name':"Note History",
                           'object_type_plural':'Notes',
                           'content':note_history,
                           'count':history_count}
        # Context
        #context['all_count'] = all_case_count
        #context['history_count'] = history_count
        #context['active_count'] = active_case_count
        context['table_objects'] = notes
        #context['case_history'] = case_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Notes'
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseNoteDetail(DetailView):
    model = CaseNote
    template_name = 'case/note/casenote_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
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
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseNoteCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseNoteCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseNoteUpdate(UpdateView):
    model = CaseNote
    template_name = 'case/note/casenote_update.html'
    form_class=CrispyCaseNoteUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('casenote_detail', kwargs={'pk': pk, 'casepk' : casepk})

    def get_context_data(self, **kwargs):
        context = super(CaseNoteUpdate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseNoteDelete(DeleteView):
    model = CaseNote
    template_name = 'case/note/casenote_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseNoteDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})


class CaseNoteList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
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

    def get_context_data(self, **kwargs):
        context = super(CaseNoteList, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


## Case Event 
class CaseEventHome(TemplateView):
    template_name = 'case/event/caseevent_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEventHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseEventHome, self).get_context_data(**kwargs)
        events = CaseEvent.objects.all()
        active_events = CaseEvent.objects.filter(status__title__icontains='active')
        event_history = []
        history_count = 0
        counts = {}
        updates = {}
        for event in events:
            event_history.append(event.history.most_recent())
            history_count += 1
        all_event_count = CaseEvent.objects.count()
        active_event_count = CaseEvent.objects.filter(status__title__icontains='active').count()
        # Count Dictionaries
        counts["history"] = {'name':"Event History",'value':history_count}
        counts["all"] = {'name':"All Events",'value':all_event_count}
        counts["active"] = {'name':"Active Events",'value':active_event_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"Active Events",
                           'object_type_plural':'Events',
                           'content':active_events,
                           'count':active_event_count}
        updates["centre"] = {'side':"centre",
                           'name':"All Events",
                           'object_type_plural':'Events',
                           'content':events,
                           'count':all_event_count}
        updates["right"] = {'side':"right",
                           'name':"Event History",
                           'object_type_plural':'Events',
                           'content':event_history,
                           'count':history_count}
        # Context
        #context['all_count'] = all_case_count
        #context['history_count'] = history_count
        #context['active_count'] = active_case_count
        context['table_objects'] = events
        #context['case_history'] = case_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Events'
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseEventDetail(DetailView):
    model = CaseEvent
    template_name = 'case/event/caseevent_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEventDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseEventDetail, self).get_context_data(**kwargs)
        return context


class CaseEventCreate(CreateView):
    model = CaseEvent
    template_name = 'case/event/caseevent_create.html'
    form_class=CrispyCaseEventCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEventCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseEventCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseEventCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseEventUpdate(UpdateView):
    model = CaseEvent
    template_name = 'case/event/caseevent_update.html'
    form_class=CrispyCaseEventUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CaseEventUpdate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEventUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('caseevent_detail', kwargs={'pk': pk, 'casepk' : casepk})


class CaseEventDelete(DeleteView):
    model = CaseEvent
    template_name = 'case/event/caseevent_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEventDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseEventDelete, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseEventList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEventList, self).dispatch(request, *args, **kwargs)

    def get(self, request):
            try:
                event_ids = []
                events = []
                for event in CaseEvent.objects.filter(case__in=self.kwargs['casepk']):
                    event_ids.append(event.pk)
                    events = CaseEvent.objects.filter(pk__in=event_ids)
            except CaseEvent.DoesNotExist:
                events = []
            return render(request, 'case/event/caseevent_list.html', {
                'objects': events,
            })

    def get_context_data(self, **kwargs):
        context = super(CaseEventList, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


def create_event(request, casepk):
    template_name = 'case/event/caseevent_create1.html'
    if request.method == 'GET':
        eventform = CaseEventCreateForm(request.GET or None)
        formset = EventPersonFormset(queryset=Person.objects.none())
    elif request.method == 'POST':
        eventform = CaseEventCreateForm(request.POST)
        formset = EventPersonFormset(request.POST)
        if eventform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            eventform.instance.case = Case.objects.get(pk=casepk)
            caseevent = eventform.save()
            for form in formset:
                # so that `book` instance can be attached.
                eventperson = form.save(commit=False)
                eventperson.event = event
                eventperson.save()
            return http.HttpResponseRedirect(caseevent.get_absolute_url())  
    return render(request, template_name, {
        'eventform': eventform,
        'formset': formset,
})


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
        tasks = CaseTask.objects.all()
        active_tasks = CaseTask.objects.filter(status__title__icontains='active')
        task_history = []
        history_count = 0
        counts = {}
        updates = {}
        for task in tasks:
            task_history.append(task.history.most_recent())
            history_count += 1
        all_task_count = CaseTask.objects.count()
        active_task_count = CaseTask.objects.filter(status__title__icontains='active').count()
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
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
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
    form_class=CrispyCaseTaskCreateForm
    
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
    form_class=CrispyCaseTaskUpdateForm

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


class CaseTaskDelete(DeleteView):
    model = CaseTask
    template_name = 'case/task/casetask_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTaskDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseTaskDelete, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


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


## Case Evidence 
class CaseEvidenceHome(TemplateView):
    template_name = 'case/evidence/caseevidence_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceHome, self).get_context_data(**kwargs)
        evidences = CaseEvidence.objects.all()
        active_evidence = CaseEvidence.objects.filter(status__title__icontains='active')
        evidence_history = []
        history_count = 0
        counts = {}
        updates = {}
        for evidence in evidences:
            evidence_history.append(evidence.history.most_recent())
            history_count += 1
        all_evidence_count = CaseEvidence.objects.count()
        active_evidence_count = CaseEvidence.objects.filter(status__title__icontains='active').count()
        # Count Dictionaries
        counts["history"] = {'name':"Evidence History",'value':history_count}
        counts["all"] = {'name':"All Evidence",'value':all_evidence_count}
        counts["active"] = {'name':"Active Evidence",'value':active_evidence_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"Active Evidence",
                           'object_type_plural':'Evidence',
                           'content':active_evidence,
                           'count':active_evidence_count}
        updates["centre"] = {'side':"centre",
                           'name':"All Evidence",
                           'object_type_plural':'Evidence',
                           'content':evidences,
                           'count':all_evidence_count}
        updates["right"] = {'side':"right",
                           'name':"Evidence History",
                           'object_type_plural':'Evidence',
                           'content':evidence_history,
                           'count':history_count}
        # Context
        #context['all_count'] = all_evidence_count
        #context['history_count'] = history_count
        #context['active_count'] = active_evidence_count
        context['table_objects'] = evidences
        #context['evidence_history'] = evidence_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Evidence'
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseEvidenceDetail(DetailView):
    model = CaseEvidence
    template_name = 'case/evidence/caseevidence_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
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
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseEvidenceCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseEvidenceUpdate(UpdateView):
    model = CaseEvidence
    template_name = 'case/evidence/caseevidence_update.html'
    form_class=CrispyCaseEvidenceUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceUpdate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
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
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEvidenceDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceDelete, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseEvidenceList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
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

    def get_context_data(self, **kwargs):
        context = super(CaseEvidenceList, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


## Case Person 
class CaseEntityHome(TemplateView):
    template_name = 'case/entity/caseentity_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseEntityHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseEntityHome, self).get_context_data(**kwargs)
        # Companies
        companies = CaseCompany.objects.all()
        all_company_count = CaseCompany.objects.count()
        active_company_count = all_company_count
        active_companies = companies
        company_history = []
        company_history_count = 0
        for company in companies:
            company_history.append(company.history.most_recent())
            company_history_count += 1        
        # People
        people = CasePerson.objects.all()
        all_person_count = CasePerson.objects.count()
        active_person_count = all_person_count
        active_people = people
        people_history = []
        people_history_count = 0
        for person in people:
            people_history.append(person.history.most_recent())
            people_history_count += 1
        # Count Dictionaries
        counts = {}
        counts["allc"] = {'name':"All Companies",'value':all_company_count}
        counts["activec"] = {'name':"Active Companies",'value':active_company_count}
        counts["historyc"] = {'name':"Company History",'value':company_history_count}
        counts["allp"] = {'name':"All People",'value':all_person_count}
        counts["activep"] = {'name':"Active People",'value':active_person_count}
        counts["historyp"] = {'name':"Person History",'value':people_history_count}
        # Updates Dictionaries
        updates = {}
        updates["left"] = {'side':"left",
                           'name':"Active People",
                           'object_type_plural':'People',
                           'content':active_people,
                           'count':active_person_count}
        updates["centre"] = {'side':"centre",
                           'name':"All People",
                           'object_type_plural':'People',
                           'content':people,
                           'count':all_person_count}
        updates["right"] = {'side':"right",
                           'name':"All Companies",
                           'object_type_plural':'Companies',
                           'content':companies,
                           'count':all_company_count}
        # Context
        context['table_objects'] = people
        context['table_objects2'] = companies
        context['person_history'] = people_history
        context['company_history'] = company_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Entities'
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CasePersonDetail(DetailView):
    model = CasePerson
    template_name = 'case/entity/caseperson_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CasePersonDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CasePersonDetail, self).get_context_data(**kwargs)
        return context


class CasePersonCreate(CreateView):
    model = CasePerson
    template_name = 'case/entity/caseperson_create.html'
    form_class = CasePersonCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CasePersonCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CasePersonCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CasePersonCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CasePersonUpdate(UpdateView):
    model = CasePerson
    template_name = 'case/entity/caseperson_update.html'
    form_class = CrispyCasePersonUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CasePersonUpdate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CasePersonUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('caseperson_detail', kwargs={'pk': pk, 'casepk' : casepk})


class CasePersonDelete(DeleteView):
    model = CasePerson
    template_name = 'case/entity/caseperson_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CasePersonDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CasePersonDelete, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


## Case Company 
class CaseCompanyDetail(DetailView):
    model = CaseCompany
    template_name = 'case/entity/casecompany_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseCompanyDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseCompanyDetail, self).get_context_data(**kwargs)
        return context


class CaseCompanyCreate(CreateView):
    model = CaseCompany
    template_name = 'case/entity/casecompany_create.html'
    form_class = CaseCompanyCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseCompanyCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseCompanyCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseCompanyCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseCompanyUpdate(UpdateView):
    model = CaseCompany
    template_name = 'case/entity/casecompany_update.html'
    form_class = CrispyCaseCompanyUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseCompanyUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('casecompany_detail', kwargs={'pk': pk, 'casepk' : casepk})

    def get_context_data(self, **kwargs):
        context = super(CaseCompanyUpdate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseCompanyDelete(DeleteView):
    model = CaseCompany
    template_name = 'case/entity/casecompany_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseCompanyDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseCompanyDelete, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


## Case Device 
class CaseDeviceHome(TemplateView):
    template_name = 'case/inventory/caseinventory_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceHome, self).get_context_data(**kwargs)
        devices = CaseInventory.objects.all()
        active_devices = devices
        device_history = []
        history_count = 0
        counts = {}
        updates = {}
        for device in devices:
            device_history.append(device.history.most_recent())
            history_count += 1
        all_device_count = CaseInventory.objects.count()
        active_device_count = all_device_count
        # Count Dictionaries
        counts["history"] = {'name':"Device History",'value':history_count}
        counts["all"] = {'name':"All Devices",'value':all_device_count}
        counts["active"] = {'name':"Active Devices",'value':active_device_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"Active Devices",
                           'object_type_plural':'Devices',
                           'content':active_devices,
                           'count':active_device_count}
        updates["centre"] = {'side':"centre",
                           'name':"All Devices",
                           'object_type_plural':'Devices',
                           'content':devices,
                           'count':all_device_count}
        updates["right"] = {'side':"right",
                           'name':"Device History",
                           'object_type_plural':'Devices',
                           'content':device_history,
                           'count':history_count}
        # Context
        #context['all_count'] = all_device_count
        #context['history_count'] = history_count
        #context['active_count'] = active_device_count
        context['table_objects'] = devices
        #context['device_history'] = device_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Devices'
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseDeviceCreate(CreateView):
    model = CaseInventory
    template_name = 'case/inventory/caseinventory_create.html'
    form_class = CrispyCaseDeviceCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseDeviceCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseDeviceDetail(DetailView):
    model = CaseInventory
    template_name = 'case/inventory/caseinventory_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceDetail, self).get_context_data(**kwargs)
        return context


class CaseDeviceUpdate(UpdateView):
    model = CaseInventory
    template_name = 'case/inventory/caseinventory_update.html'
    form_class = CrispyCaseDeviceUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CaseDeviceUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('casedevice_detail', kwargs={'pk': pk, 'casepk' : casepk})

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceUpdate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseDeviceDelete(DeleteView):
    model = CaseInventory
    template_name = 'case/inventory/caseinventory_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceDelete, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context
