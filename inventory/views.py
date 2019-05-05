## Inventory Views ##

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
from utils.forms import BootstrapAuthenticationForm
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.contrib.contenttypes.models import ContentType
from inventory.forms import DeviceCreateForm
from inventory.forms import DeviceUpdateForm
from inventory.models import Device



EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


class InventoryHome(TemplateView):
    template_name = 'inventory/inventory_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(InventoryHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InventoryHome, self).get_context_data(**kwargs)
        devices = Device.objects.all()
        available_devices = Device.objects.all()
        device_history = []
        history_count = 0
        counts = {}
        updates = {}
        for device in devices:
            device_history.append(device.history.most_recent())
            history_count += 1
        all_device_count = Device.objects.count()
        available_device_count = Device.objects.count()
        # Count Dictionaries
        counts["history"] = {'name':"Device History",'value':history_count}
        counts["all"] = {'name':"All Devices",'value':all_device_count}
        counts["active"] = {'name':"Available Devices",'value':available_device_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"All Devices",
                           'object_type_plural':'Devices',
                           'content':devices,
                           'count':all_device_count}
        updates["centre"] = {'side':"centre",
                           'name':"Available Devices",
                           'object_type_plural':'Devices',
                           'content':available_devices,
                           'count':available_device_count}
        updates["right"] = {'side':"right",
                           'name':"Devices History",
                           'object_type_plural':'Devices',
                           'content':device_history,
                           'count':history_count}
        # Context
        context['counts'] = counts
        context['updates'] = updates
        context['table_objects'] = devices
        return context


class DeviceDetail(DetailView):
    model = Device
    template_name = 'inventory/device/device_detail.html'
    context_object_name = 'device'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(DeviceDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DeviceDetail, self).get_context_data(**kwargs)
        return context

    def get_comments(self, comment_class, **kwargs):
        return comment_class.objects.filter(device__pk=self.get_object().pk)


class DeviceCreate(CreateView):
    model = Device
    template_name = 'inventory/device/device_create.html'
    form_class=DeviceCreateForm

    def get_context_data(self, **kwargs):
        context = super(DeviceCreate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(DeviceCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('device_detail', kwargs={'pk': self.object.pk})


class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceCreateForm
    template_name = 'inventory/device/device_update.html'

    def get_context_data(self, **kwargs):
        context = super(DeviceUpdate, self).get_context_data(**kwargs)
        context['pagetitle'] = 'My special Title'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(DeviceUpdate, self).dispatch(request, *args, **kwargs)


class DeviceDelete(DeleteView):
    model = Device
    success_url = reverse_lazy('devices')
    template_name = 'inventory/device/device_update.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(DeviceDelete, self).dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        """Deletes the device with the given pk.
        """
        data = {}
        Device.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully deleted device.')
        data['success'] = True
        json_data = json.dumps(data)
        return HttpResponse(json_data, mimetype="application/json")


class DevicesList(TemplateView):
    '''Index view for devices. This serves as a list view 
    for all device types.'''
    template_name = 'inventory/inventory_list.html'

    def get(self, request, **kwargs):
        #if request.user.is_authenticated():
        return super(DevicesListView, self).get(request)
        #else:
            #return super(DevicesListView, self).get(request)
            #return redirect('home')

    def get_context_data(self, **kwargs):
        device_type = self.kwargs['device_type']
        device_class = None
        if device_type == 'ipads':
            device_class = Ipad
        elif device_type == 'headphones':
            device_class = Headphones
        elif device_type == 'adapters':
            device_class = Adapter
        elif device_type == 'cases':
            device_class = Case

        context = super(DevicesListView, self).get_context_data(**kwargs)
        context['contenttype_id'] = ContentType.objects.get_for_model(device_class).pk
        context['objects'] = device_class.objects.all()
        context['device_type'] = self.kwargs['device_type']
        return context