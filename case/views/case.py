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

"""  
    Note:
    
    Example:

	Args:

	Attributes:

    Returns:

    Raises:

	"""

## Case 
class CaseHome(TemplateView):
    """  View for Case index Page

	"""
    template_name = 'case/case/case_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """  Defines context data for page

        Returns:
            table_objects : All Cases
            case_history : All Case  history
            counts : Case count
            updates : Predfined fields for update section
            object_type_plural : Object plural


	    """
        context = super(CaseHome, self).get_context_data(**kwargs)
        cases = Case.objects.all()
        active_cases = Case.objects.active()
        case_history = []
        history_count = 0
        counts = {}
        updates = {}
        for case in cases:
            case_history.append(case.history.most_recent())
            history_count += 1
        all_case_count = cases.count()
        active_case_count = active_cases.count()
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
        context['table_objects'] = cases
        #context['case_history'] = case_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Cases'
        return context


class CaseDetail(DetailView):
    """  
    Note:
    
    Example:

	Args:

	Attributes:

    Returns:

    Raises:

	"""
    model = Case
    template_name = 'case/case/case_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """  
        Note:
    
        Example:

	    Args:

	    Attributes:

        Returns:

        Raises:

	    """
        context = super(CaseDetail, self).get_context_data(**kwargs)
        context['events'] = CaseEvent.objects.filter(case=self.object.pk)
        context['evidence'] = CaseEvidence.objects.filter(case=self.object.pk)
        context['tasks'] = CaseTask.objects.filter(case=self.object.pk)
        context['persons'] = CasePerson.objects.filter(case=self.object.pk)
        context['companies'] = CaseCompany.objects.filter(case=self.object.pk)
        context['devices'] = CaseInventory.objects.filter(case=self.object.pk)
        return context

    
class CaseCreate(CreateView):
    """  
    Note:
    
    Example:

	Args:

	Attributes:

    Returns:

    Raises:

	"""
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
    """  
    Note:
    
    Example:

	Args:

	Attributes:

    Returns:

    Raises:

	"""
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


class CaseTable(SingleTableView):
    """  
    Note:
    
    Example:

	Args:

	Attributes:

    Returns:

    Raises:

	"""
    model = Case
    table_class = CaseTable

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseTable, self).dispatch(request, *args, **kwargs)


class CaseList(ListView):
    """  
    Note:
    
    Example:

	Args:

	Attributes:

    Returns:

    Raises:

	"""
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
    """  
    Note:
    
    Example:

	Args:

	Attributes:

    Returns:

    Raises:

	"""
    table = Case.objects.all()
    #RequestConfig(request).configure(table)
    return render(request, 'case/case_table.html', { 'table' : table })


               
#def case_filter(request):
#    filter = CaseFilter(request.GET, queryset=Case.objects.all())
#    return render(request, 'case/case_filter.html', {'filter': filter})

