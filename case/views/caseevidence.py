## Case Evidence Views ##

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
from case.models import CaseEvidence
from case.forms.evidence import CaseEvidenceCreateForm
from case.forms.evidence import CaseEvidenceUpdateForm


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
        thiscase = Case.objects.get(pk=self.kwargs['casepk'])
        evidences = CaseEvidence.objects.filter(case=thiscase).all()
        active_evidence = CaseEvidence.objects.filter(case=thiscase).filter(status__title__icontains='active')
        evidence_history = []
        history_count = 0
        counts = {}
        updates = {}
        for evidence in evidences:
            evidence_history.append(evidence.history.most_recent())
            history_count += 1
        all_evidence_count = CaseEvidence.objects.filter(case=thiscase).count()
        active_evidence_count = CaseEvidence.objects.filter(case=thiscase).filter(status__title__icontains='active').count()
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
        context['object'] = thiscase
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
    form_class=CaseEvidenceCreateForm
    
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
    form_class=CaseEvidenceUpdateForm

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

