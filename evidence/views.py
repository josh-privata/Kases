"""
Evidence views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from evidence.forms import EvidenceCreateForm, EvidenceEditForm, CrispyEvidenceForm
from evidence.models import Evidence
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from evidence.tables import EvidenceTable, FullEvidenceTable
from django_tables2 import RequestConfig, SingleTableView
from django.urls import reverse
from django.shortcuts import get_object_or_404
import base.views


#class AjaxableResponseMixin:
#    """
#    Mixin to add AJAX support to a form.
#    Must be used with an object-based FormView (e.g. CreateView)
#    """
#    def form_invalid(self, form):
#        response = super().form_invalid(form)
#        if self.request.is_ajax():
#            return JsonResponse(form.errors, status=400)
#        else:
#            return response

#    def form_valid(self, form):
#        # We make sure to call the parent's form_valid() method because
#        # it might do some processing (in the evidence of CreateView, it will
#        # call form.save() for example).
#        response = super().form_valid(form)
#        if self.request.is_ajax():
#            data = {
#                'pk': self.object.pk,
#            }
#            return JsonResponse(data)
#        else:
#            return response
        
## Evidence Main
#class EvidenceHome(TemplateView):
#    template_name = 'evidence/evidence_index.html'

#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            form = base.forms.BootstrapAuthenticationForm()
#            return render(request, 'registration/login.html', {'form': form})
#        else:
#            return super(EvidenceHome, self).dispatch(request, *args, **kwargs)

#    def get_context_data(self, **kwargs):
#        context = super(EvidenceHome, self).get_context_data(**kwargs)
#        evidences = Evidence.objects.all()
#        context['objects1'] = evidences
#        context['objects2'] = evidences
#        context['objects3'] = evidences
#        context['table_objects'] = evidences
#        evidence_history = []
#        history_count = 0
#        for evidence in evidences:
#            evidence_history.append(evidence.history.most_recent())
#            history_count += 1
#        context['evidence_history'] = evidence_history
#        context['history_count'] = history_count
#        context['active_count'] = Evidence.objects.filter(status__title__icontains='active').count()
#        context['all_count'] = Evidence.objects.count()
#        return context


#class EvidenceDetail(DetailView):
#    model = Evidence
#    template_name_suffix = '_detail'

#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            form = base.forms.BootstrapAuthenticationForm()
#            return render(request, 'registration/login.html', {'form': form})
#        else:
#            return super(EvidenceDetail, self).dispatch(request, *args, **kwargs)

#    def get_context_data(self, **kwargs):
#        context = super(EvidenceDetail, self).get_context_data(**kwargs)
#        return context


#class EvidenceCreate(CreateView):
#    model = Evidence
#    template_name_suffix = '_create'
#    form_class=CrispyEvidenceForm

#    def get_context_data(self, **kwargs):
#        context = super(EvidenceCreate, self).get_context_data(**kwargs)
#        context['pagetitle'] = 'My special Title'
#        return context

#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            form = base.forms.BootstrapAuthenticationForm()
#            return render(request, 'registration/login.html', {'form': form})
#        else:
#            return super(EvidenceCreate, self).dispatch(request, *args, **kwargs)

#    def get_success_url(self, **kwargs):
#        return reverse('evidence_detail', kwargs={'pk': self.object.pk})


#class EvidenceUpdate(UpdateView):
#    model = Evidence
#    form_class=EvidenceEditForm
#    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief', 'comment', 'private', 'type', 'status',
#    #             'classification', 'priority', 'authorisation', 'image_upload']
#    template_name_suffix = '_update'

#    def get_context_data(self, **kwargs):
#        context = super(EvidenceUpdate, self).get_context_data(**kwargs)
#        context['pagetitle'] = 'My special Title'
#        return context

#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            form = base.forms.BootstrapAuthenticationForm()
#            return render(request, 'registration/login.html', {'form': form})
#        else:
#            return super(EvidenceUpdate, self).dispatch(request, *args, **kwargs)


#class EvidenceDelete(DeleteView):
#    model = Evidence
#    success_url = reverse_lazy('evidence_list')
#    template_name = 'evidence/evidence_delete.html'
    
#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            form = base.forms.BootstrapAuthenticationForm()
#            return render(request, 'registration/login.html', {'form': form})
#        else:
#            return super(EvidenceDelete, self).dispatch(request, *args, **kwargs)


## Evidence Displays
#class EvidenceTable(SingleTableView):
#    model = Evidence
#    table_class = FullEvidenceTable

#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            form = base.forms.BootstrapAuthenticationForm()
#            return render(request, 'registration/login.html', {'form': form})
#        else:
#            return super(EvidenceTable, self).dispatch(request, *args, **kwargs)


#class EvidenceList(ListView):
#    paginate_by = 1

#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            form = base.forms.BootstrapAuthenticationForm()
#            return render(request, 'registration/login.html', {'form': form})
#        else:
#            return super(EvidenceList, self).dispatch(request, *args, **kwargs)

#    def get(self, request):
#            try:
#                evidence_ids = []
#                evidences = []
#                for evidence in Evidence.objects.all():
#                    evidence_ids.append(evidence.pk)
#                    evidences = Evidence.objects.filter(pk__in=evidence_ids)
#            except Evidence.DoesNotExist:
#                evidences = []
#            return render(request, 'evidence/evidence_list.html', {
#                'objects': evidences,
#            })


# #Evidence Notes
##class EvidenceNoteCreate(CreateView):
##    model = EvidenceNote
##    template_name = 'evidence/note/evidencenote_create.html'
##    form_class=EvidenceNoteCreateForm
##    evidence = None
    
##    def dispatch(self, request, *args, **kwargs):
##        if not request.user.is_authenticated:
##            form = base.forms.BootstrapAuthenticationForm()
##            return render(request, 'registration/login.html', {'form': form})
##        else:
##            return super(EvidenceNoteCreate, self).dispatch(request, *args, **kwargs)

##    def get_success_url(self, **kwargs):
##        return reverse("evidence_detail", kwargs={'pk': self.object.pk})

##    def get(self, request, *args, **kwargs):
##        self.object = None
##        evidencepk = kwargs.get('evidencepk')
##        self.evidence = Evidence.objects.get(pk=evidencepk)
##        context_data = self.get_context_data()
##        context_data.update(evidence=self.evidence)
##        return self.render_to_response(context_data)  

##    def get_form_kwargs(self):
##        kwargs = super(EvidenceNoteCreate, self).get_form_kwargs()
##        kwargs.update({'evidence': self.evidence})
##        return kwargs


##class EvidenceNoteUpdate(UpdateView):
##    model = EvidenceNote
##    form_class=EvidenceNoteEditForm
##    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief', 'comment', 'private', 'type', 'status',
##    #             'classification', 'priority', 'authorisation', 'image_upload']
##    template_name_suffix = 'note_update'


##class EvidenceNoteDelete(DeleteView):
##    model = EvidenceNote
##    success_url = reverse_lazy('evidencenote_list')


## Evidence Tasksw_evidence.html', {'form': form})