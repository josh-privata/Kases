## Event Views ##

from django.shortcuts import render
from event.forms import EventEditForm, CrispyEventForm
from event.models import Event
from django.http import JsonResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from event.tables import EventTable, FullEventTable
from django_tables2 import SingleTableView
from django.urls import reverse
import base.views


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
        # it might do some processing (in the event of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
        

# Main Views
class EventHome(TemplateView):
    template_name = 'event/event_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(EventHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventHome, self).get_context_data(**kwargs)
        events = Event.objects.all()
        context['objects1'] = events
        context['objects2'] = events
        context['objects3'] = events
        context['table_objects'] = events
        event_history = []
        history_count = 0
        for event in events:
            event_history.append(event.history.most_recent())
            history_count += 1
        context['event_history'] = event_history
        context['history_count'] = history_count
        context['active_count'] = Event.objects.filter(status__title__icontains='active').count()
        context['all_count'] = Event.objects.count()
        return context


## Detail Views
class EventDetail(DetailView):
    model = Event
    template_name_suffix = '_detail'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(EventDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        return context


## Create Views
class EventCreate(CreateView):
    model = Event
    template_name_suffix = '_create'
    form_class=CrispyEventForm

    def get_context_data(self, **kwargs):
        context = super(EventCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(EventCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('event_detail', kwargs={'pk': self.object.pk})


## Update Views
class EventUpdate(UpdateView):
    model = Event
    form_class=EventEditForm
    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief', 'comment', 'private', 'type', 'status',
    #             'classification', 'priority', 'authorisation', 'image_upload']
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(EventUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(EventUpdate, self).dispatch(request, *args, **kwargs)


## Delete Views
class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')
    template_name = 'event/event_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(EventDelete, self).dispatch(request, *args, **kwargs)


# Event Displays
class EventTable(SingleTableView):
    model = Event
    table_class = FullEventTable

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(EventTable, self).dispatch(request, *args, **kwargs)


## List Views
class EventList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(EventList, self).dispatch(request, *args, **kwargs)

    def get(self, request):
            try:
                event_ids = []
                events = []
                for event in Event.objects.all():
                    event_ids.append(event.pk)
                    events = Event.objects.filter(pk__in=event_ids)
            except Event.DoesNotExist:
                events = []
            return render(request, 'event/event_list.html', {
                'objects': events,
            })