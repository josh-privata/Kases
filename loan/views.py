## Loan Views ##

import re
#from django.utils import simplejson as json
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
#from inventory.forms import LoanCreateForm, LoanUpdateForm
from loan.forms import LoanCreateForm, LoanUpdateForm
from loan.forms import LoanWithBothCreateForm, LoanWithCaseCreateForm
from loan.forms import LoanWithDeviceCreateForm
from loan.forms import LoanWithBothUpdateForm, LoanWithCaseUpdateForm, LoanWithDeviceUpdateForm
from loan.models import Loan
from case.models import Case
from inventory.models import Device
from utils.forms import BootstrapAuthenticationForm


## Loan Views
class LoanHome(TemplateView):
    template_name = 'loan/loan/loan_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoanHome, self).get_context_data(**kwargs)

        # Empty Variables
        loan_history = []
        all_loan_count = 0
        available_loan_count = 0
        history_count = 0
        counts = {}
        updates = {}
        device = None 
        case = None

        # Determine Sender
        try: device = self.kwargs['devicepk']
        except: pass        
        try: case = self.kwargs['casepk']
        except: pass  
        
        # Sent Via Case
        if case != None:
            loans = Loan.objects.filter(case__pk=case)
            available_loans = Loan.objects.filter(case__pk=case)
            all_loan_count = Loan.objects.filter(case__pk=case).count()
            available_loant_count = Loan.objects.filter(case__pk=case).count()
            context['sidebar'] = 'case'
            context['object'] = Case.objects.get(pk=self.kwargs['casepk'])

        # Sent Via Inventory
        elif device != None:
            loans = Loan.objects.filter(device__pk=device)
            available_loans = Loan.objects.filter(device__pk=device)
            all_loan_count = Loan.objects.filter(device__pk=device).count()
            available_loant_count = Loan.objects.filter(device__pk=device).count()
            context['sidebar'] = 'device'

        # Sent Via Loans
        else:
            loans = Loan.objects.all()
            available_loans = Loan.objects.all()
            all_loan_count = Loan.objects.all().count()
            available_loant_count = Loan.objects.all().count()

        # Get Loan Context History
        for loan in loans:
            loan_history.append(loan.history.most_recent())
            history_count += 1
        
        # Count Dictionaries
        counts["history"] = {'name':"Loan History",'value':history_count}
        counts["all"] = {'name':"All Loans",'value':all_loan_count}
        counts["active"] = {'name':"Available Loans",'value':available_loan_count}
        
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"All Loans",
                           'object_type_plural':'Loans',
                           'content':loans,
                           'count':all_loan_count}
        updates["centre"] = {'side':"centre",
                           'name':"Available Loans",
                           'object_type_plural':'Loans',
                           'content':available_loans,
                           'count':available_loan_count}
        updates["right"] = {'side':"right",
                           'name':"Loans History",
                           'object_type_plural':'Loans',
                           'content':loan_history,
                           'count':history_count}
        
        # Define Context
        context['counts'] = counts
        context['updates'] = updates
        context['table_objects'] = loans
        return context


class LoanDetail(DetailView):
    model = Loan
    template_name = 'loan/loan/loan_detail.html'
    context_object_name = 'loan'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoanDetail, self).get_context_data(**kwargs)
        return context

    def get_comments(self, comment_class, **kwargs):
        return comment_class.objects.filter(loan__pk=self.get_object().pk)


class LoanCreate(CreateView):
    model = Loan
    template_name = 'loan/loan/loan_create.html'
    form_class=LoanCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('loan_detail', kwargs={'pk': self.object.pk})


class LoanUpdate(UpdateView):
    model = Loan
    form_class = LoanUpdateForm
    template_name = 'loan/loan/loan_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanUpdate, self).dispatch(request, *args, **kwargs)


class LoanDelete(DeleteView):
    model = Loan
    success_url = reverse_lazy('loans')
    template_name = 'loan/loan/loan_update.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanDelete, self).dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        """Deletes the loan with the given pk.
        """
        data = {}
        Loan.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully deleted loan.')
        data['success'] = True
        json_data = json.dumps(data)
        return HttpResponse(json_data, mimetype="application/json")


class LoanList(TemplateView):
    '''Index view for loans. This serves as a list view 
    for all loan types.'''
    template_name = 'loan/loan/loan_list.html'

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanList, self).get(request)


## Loan With Case
class LoanCreateWithCase(CreateView):
    model = Loan
    template_name = 'loan/loan/loan_create.html'
    form_class=LoanWithCaseCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanCreateWithCase, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        casepk = self.kwargs['casepk']
        return reverse('loanwithcase_detail', kwargs={'pk': self.object.pk, 'casepk' : casepk})

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(LoanCreateWithCase, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoanCreateWithCase, self).get_context_data(**kwargs)
        context['case'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class LoanUpdateWithCase(CreateView):
    model = Loan
    template_name = 'loan/loan/loan_create.html'
    form_class=LoanWithCaseUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanUpdateWithCase, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        casepk = self.kwargs['casepk']
        return reverse('loanwithcase_detail', kwargs={'pk': self.object.pk, 'casepk' : casepk})

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(LoanUpdateWithCase, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoanUpdateWithCase, self).get_context_data(**kwargs)
        context['case'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


# Loan With Device
class LoanCreateWithDevice(CreateView):
    model = Loan
    template_name = 'loan/loan/loan_create.html'
    form_class=LoanWithDeviceCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanCreateWithDevice, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        devicepk = self.kwargs['devicepk']
        return reverse('loanwithdevice_detail', kwargs={'pk': self.object.pk, 'devicepk' : devicepk})

    def form_valid(self, form):
        form.instance.device = Device.objects.get(pk=self.kwargs['devicepk'])
        return super(LoanCreateWithDevice, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoanCreateWithDevice, self).get_context_data(**kwargs)
        context['device'] = Case.objects.get(pk=self.kwargs['devicepk'])
        return context


class LoanUpdateWithDevice(CreateView):
    model = Loan
    template_name = 'loan/loan/loan_create.html'
    form_class=LoanWithDeviceUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanUpdateWithDevice, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        devicepk = self.kwargs['devicepk']
        return reverse('loanwithdevice_detail', kwargs={'pk': self.object.pk, 'devicepk' : devicepk})

    def form_valid(self, form):
        form.instance.device = Device.objects.get(pk=self.kwargs['devicepk'])
        return super(LoanUpdateWithDevice, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoanUpdateWithDevice, self).get_context_data(**kwargs)
        context['device'] = Case.objects.get(pk=self.kwargs['devicepk'])
        return context


# Loan With Both
class LoanCreateWithBoth(CreateView):
    model = Loan
    template_name = 'loan/loan/loan_create.html'
    form_class=LoanWithBothCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanCreateWithBoth, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        casepk = self.kwargs['casepk']
        devicepk = self.kwargs['devicepk']
        return reverse('loanwithboth_detail', kwargs={'pk': self.object.pk, 'casepk' : casepk, 'devicepk' : devicepk})

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        form.instance.case = Device.objects.get(pk=self.kwargs['devicepk'])
        return super(LoanCreateWithBoth, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoanCreateWithBoth, self).get_context_data(**kwargs)
        context['device'] = Case.objects.get(pk=self.kwargs['devicepk'])
        context['case'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class LoanUpdateWithBoth(CreateView):
    model = Loan
    template_name = 'loan/loan/loan_create.html'
    form_class=LoanWithBothUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanUpdateWithBoth, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        casepk = self.kwargs['casepk']
        devicepk = self.kwargs['devicepk']
        return reverse('loanwithboth_detail', kwargs={'pk': self.object.pk, 'casepk' : casepk, 'devicepk' : devicepk})

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        form.instance.case = Device.objects.get(pk=self.kwargs['devicepk'])
        return super(LoanUpdateWithBoth, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoanUpdateWithBoth, self).get_context_data(**kwargs)
        context['device'] = Case.objects.get(pk=self.kwargs['devicepk'])
        context['case'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


## Loan Admin Views

#    def get_context_data(self, **kwargs):
#        context = super(LoanRequestHome, self).get_context_data(**kwargs)
#        loanrequest_history = []
#        history_count = 0
#        counts = {}
#        updates = {}
#        device = None 
#        case = None

#        try: device = self.kwargs['devicepk']
#        except: pass        
#        try: case = self.kwargs['casepk']
#        except: pass  

#        if case != None:
#            loanrequests = LoanRequest.objects.filter(case__pk=case)
#            available_loanrequests = LoanRequest.objects.filter(case__pk=case)
#            all_loanrequest_count = LoanRequest.objects.filter(case__pk=case).count()
#            available_loanrequest_count = LoanRequest.objects.filter(case__pk=case).count()
#            context['sidebar'] = 'case'
#            context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
#        elif device != None:
#            loanrequests = LoanRequest.objects.filter(device__pk=device)
#            available_loanrequests = LoanRequest.objects.filter(device__pk=device)
#            all_loanrequest_count = LoanRequest.objects.filter(device__pk=device).count()
#            available_loanrequest_count = LoanRequest.objects.filter(device__pk=device).count()
#            context['sidebar'] = 'device'
#        else:
#            loanrequests = LoanRequest.objects.all()
#            available_loanrequests = LoanRequest.objects.all()
#            all_loanrequest_count = LoanRequest.objects.count()
#            available_loanrequest_count = LoanRequest.objects.count()

#        for loan in loanrequests:
#            loanrequest_history.append(loan.history.most_recent())
#            history_count += 1

#        # Count Dictionaries
#        counts["history"] = {'name':"Loan History",'value':history_count}
#        counts["all"] = {'name':"All Loans",'value':all_loanrequest_count}
#        counts["active"] = {'name':"Available Loans",'value':available_loanrequest_count}

#        # Updates Dictionaries
#        updates["left"] = {'side':"left",
#                           'name':"All Loans",
#                           'object_type_plural':'Loans',
#                           'content':loanrequests,
#                           'count':all_loanrequest_count}
#        updates["centre"] = {'side':"centre",
#                           'name':"Available Loans",
#                           'object_type_plural':'Loans',
#                           'content':available_loanrequests,
#                           'count':available_loanrequest_count}
#        updates["right"] = {'side':"right",
#                           'name':"Loans History",
#                           'object_type_plural':'Loans',
#                           'content':loanrequest_history,
#                           'count':history_count}
        
#        # Context
#        context['counts'] = counts
#        context['updates'] = updates
#        context['table_objects'] = loanrequests
#        return context

