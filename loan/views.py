## Loan Views ##

import re
from django import http
from django.shortcuts import render
#from django.utils import simplejson as json
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django_tables2 import SingleTableView
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.contrib.contenttypes.models import ContentType
#from inventory.forms import LoanCreateForm, LoanUpdateForm
from loan.forms import CrispyLoanCreateForm, CrispyLoanUpdateForm
from loan.models import Loan
from utils.forms import BootstrapAuthenticationForm


EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

## Main View 
class LoanHome(TemplateView):
    template_name = 'loan/loan_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(LoanHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoanHome, self).get_context_data(**kwargs)
        loans = Loan.objects.all()
        available_loans = Loan.objects.all()
        loan_history = []
        history_count = 0
        counts = {}
        updates = {}
        for loan in loans:
            loan_history.append(loan.history.most_recent())
            history_count += 1
        all_loan_count = Loan.objects.count()
        available_loan_count = Loan.objects.count()
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
        # Context
        context['counts'] = counts
        context['updates'] = updates
        context['table_objects'] = loans
        return context


### Abstract Views ###
class LoanDetail(DetailView):
    model = Loan
    template_name = 'loan/loan_detail.html'
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
    template_name = 'loan/loan_create.html'
    form_class=CrispyLoanCreateForm

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
    form_class = CrispyLoanCreateForm
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
    template_name = 'loan/loan_update.html'
    
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


#class CommentUpdate(UpdateView):
#    '''An abstract CommentEdit View.'''
#    template_name = 'loan/edit_comment.html'
#    # Must define the comment model to update, like so:
#    # model = IpadComment
#    form_class = CommentUpdateForm
#    pk_url_kwarg = 'comment_id'

#    def get_success_url(self):
#        """On success, redirect to the loan's detail page."""
#        comment = self.get_object()
#        return comment.loan_url


#class CommentDelete(DeleteView):
#    '''An abstract CommentDelete View.'''

#    def get_comment_class(self):
#        """Returns the comment class corresponding to a 
#        specific loan type. Must be implemented by descendant classes.
        
#        Example:
#            return IpadComment
#        """
#        raise NotImplementedError

#    def post(self, request, loan_id, comment_id):
#        response_data = {}
#        # Delete the comment
#        comment_class = self.get_comment_class()
#        comment_class.objects.filter(pk=comment_id).delete()
#        # Display a message
#        messages.success(request, 'Successfully deleted comment.')
#        response_data['success'] = True
#        response_data['pk'] = comment_id
#        json_data = json.dumps(response_data)
#        return HttpResponse(json_data, mimetype='application/json')


class LoansList(TemplateView):
    '''Index view for loans. This serves as a list view 
    for all loan types.'''
    template_name = 'loan/loan_list.html'

    def get(self, request, **kwargs):
        #if request.user.is_authenticated():
        return super(LoansListView, self).get(request)
        #else:
            #return super(LoansListView, self).get(request)
            #return redirect('home')
