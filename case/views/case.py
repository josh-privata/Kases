## Case Views ##

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django_tables2 import SingleTableView
#from case.filters import CaseFilter
from utils.forms import BootstrapAuthenticationForm
from case.models import Case
from case.models import CaseTask
from case.models import CaseEvidence
from case.models import CasePerson
from case.models import CaseCompany
from case.models import CaseInventory
from case.models import CaseEvent
from case.tables import CaseTable
from case.forms.case import CaseForm
from case.forms.case import CaseUpdateForm


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
        updates["left2"] = {'side':"left2",
                           'name':"Active Cases",
                           'object_type_plural':'Cases',
                           'content':active_cases,
                           'count':active_case_count}
        updates["centre2"] = {'side':"centre2",
                           'name':"All Cases",
                           'object_type_plural':'Cases',
                           'content':cases,
                           'count':all_case_count}
        updates["right2"] = {'side':"right2",
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
        #context['notes'] = CaseNote.objects.filter(case=self.object.pk)
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
    form_class=CaseForm

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
    form_class = CaseUpdateForm
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

