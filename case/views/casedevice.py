## Case Device Views ##

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
from case.models import CaseInventory
from case.forms.device import CaseDeviceCreateForm
from case.forms.device import CaseDeviceUpdateForm


## Case Device 
class CaseDeviceHome(TemplateView):
    template_name = 'case/inventory/caseinventory_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceHome, self).get_context_data(**kwargs)
        thiscase = Case.objects.get(pk=self.kwargs['casepk'])
        devices = CaseInventory.objects.filter(case=thiscase).all()
        active_devices = devices
        device_history = []
        history_count = 0
        counts = {}
        updates = {}
        for device in devices:
            device_history.append(device.history.most_recent())
            history_count += 1
        all_device_count = CaseInventory.objects.filter(case=thiscase).count()
        active_device_count = all_device_count
        # Count Dictionaries
        counts["history"] = {'name':"Device History",'value':history_count}
        counts["all"] = {'name':"All Devices",'value':all_device_count}
        counts["active"] = {'name':"Active Devices",'value':active_device_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"Active Devices",
                           'object_type_plural':'Devices',
                           'content':active_devices,
                           'count':active_device_count}
        updates["centre"] = {'side':"centre",
                           'name':"All Devices",
                           'object_type_plural':'Devices',
                           'content':devices,
                           'count':all_device_count}
        updates["right"] = {'side':"right",
                           'name':"Device History",
                           'object_type_plural':'Devices',
                           'content':device_history,
                           'count':history_count}
        # Context
        #context['all_count'] = all_device_count
        #context['history_count'] = history_count
        #context['active_count'] = active_device_count
        context['table_objects'] = devices
        #context['device_history'] = device_history
        context['counts'] = counts
        context['updates'] = updates
        context['object_type_plural'] = 'Devices'
        context['object'] = thiscase
        return context


class CaseDeviceDetail(DetailView):
    model = CaseInventory
    template_name = 'case/inventory/caseinventory_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceDetail, self).get_context_data(**kwargs)
        return context


class CaseDeviceCreate(CreateView):
    model = CaseInventory
    template_name = 'case/inventory/caseinventory_create.html'
    form_class = CaseDeviceCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = Case.objects.get(pk=self.kwargs['casepk'])
        return super(CaseDeviceCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['casepk']
        return reverse('case_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceCreate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context


class CaseDeviceUpdate(UpdateView):
    model = CaseInventory
    template_name = 'case/inventory/caseinventory_update.html'
    form_class = CaseDeviceUpdateForm

    #fields = ['title', 'reference', 'background', 'location', 'description', 'brief',
    #           'comment', 'private', 'type', 'status', 'classification', 'priority',
    #           'authorisation', 'image_upload']
    
    def get_context_data(self, **kwargs):
        context = super(CaseDeviceUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(CaseDeviceUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        casepk = self.kwargs['casepk']
        return reverse('casedevice_detail', kwargs={'pk': pk, 'casepk' : casepk})

    def get_context_data(self, **kwargs):
        context = super(CaseDeviceUpdate, self).get_context_data(**kwargs)
        context['object'] = Case.objects.get(pk=self.kwargs['casepk'])
        return context
