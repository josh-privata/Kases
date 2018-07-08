from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import (Http404, HttpResponseForbidden,
                         HttpResponseServerError, HttpResponseRedirect)
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from entity.models import Company
from entity.forms import CompanyCreateForm, CompanyEditForm, CompanyFormSet, AddressForm
from django.urls import reverse_lazy


class CompanyCreate(TemplateView):

    template_name = 'entity/company/company_create.html'

    def get(self, request, *args, **kwargs):
        company_form = CompanyCreateForm(self.request.GET or None)
        address_form = AddressForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['company_form'] = company_form
        context['address_form'] = address_form
        return self.render_to_response(context)

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['company_form'] = PostForm()
        #return context


class CompanyFormView(FormView):
    form_class = CompanyCreateForm
    template_name = 'entity/company/company_create.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        company_form = self.form_class(request.POST)
        address_form = AddressForm()
        if company_form.is_valid():
            company_form.save()
            return self.render_to_response(
                self.get_context_data(
                success=True
            )
        )
        else:
        return self.render_to_response(
        self.get_context_data(
                company_form=company_form,
   
        )


class CompanyDetail(DetailView):

    model = Company
    template_name = 'entity/company/company_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetail, self).get_context_data(**kwargs)
        return context


class CompanyCreate1(CreateView):
    model = Company
    template_name = 'entity/company/company_create.html'

    def get_success_url(self, **kwargs):
        return reverse('company_detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        formset = CompanyFormSet()
        return formset

class CompanyUpdate(UpdateView):
    model = Company
    form_class=CompanyFormSet
    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief', 'comment', 'private', 'type', 'status',
    #             'classification', 'priority', 'authorisation', 'image_upload']
    template_name = 'entity/company/company_update.html'


class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('company_list')
    template_name = 'entity/company/company_delete.html'


def list(request, page=1, template='entity/company/company_list.html'):
    """List of all the comapnies.

    :param template: Add a custom template.
    """

    company_list = Company.objects.all()
    paginator = Paginator(company_list, 20)

    try:
        companies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        companies = paginator.page(paginator.num_pages)

    kwvars = {
        'object_list': companies.object_list,
        'has_next': companies.has_next(),
        'has_previous': companies.has_previous(),
        'has_other_pages': companies.has_other_pages(),
        'start_index': companies.start_index(),
        'end_index': companies.end_index(),
    }

    try:
        kwvars['previous_page_number'] = companies.previous_page_number()
    except (EmptyPage, InvalidPage):
        kwvars['previous_page_number'] = None
    try:
        kwvars['next_page_number'] = companies.next_page_number()
    except (EmptyPage, InvalidPage):
        kwvars['next_page_number'] = None

