## Case Event Views ##

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
from case.models import CaseEvent
from case.forms.event import CaseEventCreateForm
from case.forms.event import CaseEventUpdateForm


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
        thiscase = Case.objects.get(pk=self.kwargs['casepk'])
        events = CaseEvent.objects.filter(case=thiscase).all()
        active_events = CaseEvent.objects.filter(case=thiscase).filter(status__title__icontains='active')
        event_history = []
        history_count = 0
        counts = {}
        updates = {}
        for event in events:
            event_history.append(event.history.most_recent())
            history_count += 1
        all_event_count = CaseEvent.objects.filter(case=thiscase).count()
        active_event_count = CaseEvent.objects.filter(case=thiscase).filter(status__title__icontains='active').count()
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
        context['object'] = thiscase
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
    form_class=CaseEventCreateForm
    
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
    form_class=CaseEventUpdateForm

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
