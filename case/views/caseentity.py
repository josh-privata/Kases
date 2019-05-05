## Case Entity Views ##

from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
#from case.filters import CaseFilter
from utils.forms import BootstrapAuthenticationForm
from case.models import Case
from case.models import CasePerson
from case.models import CaseCompany
from case.forms.entity import CaseCompanyCreateForm
from case.forms.entity import CaseCompanyUpdateForm
from case.forms.entity import CasePersonCreateForm
from case.forms.entity import CasePersonUpdateForm


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
        thiscase = Case.objects.get(pk=self.kwargs['casepk'])
        # Companies
        companies = CaseCompany.objects.filter(case=thiscase).all()
        all_company_count = CaseCompany.objects.filter(case=thiscase).count()
        active_company_count = all_company_count
        active_companies = companies
        company_history = []
        company_history_count = 0
        for company in companies:
            company_history.append(company.history.most_recent())
            company_history_count += 1        
        # People
        people = CasePerson.objects.filter(case=thiscase).all()
        all_person_count = CasePerson.objects.filter(case=thiscase).count()
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
        context['object'] = thiscase
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
    form_class = CasePersonUpdateForm

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
    form_class = CaseCompanyUpdateForm

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
