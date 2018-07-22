## Note Views ##

from django.shortcuts import render
from note.forms import NoteEditForm, CrispyNoteForm
from note.models import Note
from django.http import JsonResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from note.tables import NoteTable, FullNoteTable
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
        # it might do some processing (in the note of CreateView, it will
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
class NoteHome(TemplateView):
    template_name = 'note/note_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(NoteHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NoteHome, self).get_context_data(**kwargs)
        notes = Note.objects.all()
        context['objects1'] = notes
        context['objects2'] = notes
        context['objects3'] = notes
        context['table_objects'] = notes
        note_history = []
        history_count = 0
        for note in notes:
            note_history.append(note.history.most_recent())
            history_count += 1
        context['note_history'] = note_history
        context['history_count'] = history_count
        context['active_count'] = Note.objects.filter(status__title__icontains='active').count()
        context['all_count'] = Note.objects.count()
        return context


## Detail Views
class NoteDetail(DetailView):
    model = Note
    template_name_suffix = '_detail'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(NoteDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NoteDetail, self).get_context_data(**kwargs)
        return context


## Create Views
class NoteCreate(CreateView):
    model = Note
    template_name_suffix = '_create'
    form_class=CrispyNoteForm

    def get_context_data(self, **kwargs):
        context = super(NoteCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(NoteCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('note_detail', kwargs={'pk': self.object.pk})


## Update Views
class NoteUpdate(UpdateView):
    model = Note
    form_class=NoteEditForm
    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief', 'comment', 'private', 'type', 'status',
    #             'classification', 'priority', 'authorisation', 'image_upload']
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(NoteUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(NoteUpdate, self).dispatch(request, *args, **kwargs)


## Delete Views
class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('note_list')
    template_name = 'note/note_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(NoteDelete, self).dispatch(request, *args, **kwargs)


# Note Displays
class NoteTable(SingleTableView):
    model = Note
    table_class = FullNoteTable

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(NoteTable, self).dispatch(request, *args, **kwargs)


## List Views
class NoteList(ListView):
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(NoteList, self).dispatch(request, *args, **kwargs)

    def get(self, request):
            try:
                note_ids = []
                notes = []
                for note in Note.objects.all():
                    note_ids.append(note.pk)
                    notes = Note.objects.filter(pk__in=note_ids)
            except Note.DoesNotExist:
                notes = []
            return render(request, 'note/note_list.html', {
                'objects': notes,
            })