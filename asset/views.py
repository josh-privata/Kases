## Asset Views ##

import re
#from django.utils import simplejson as json
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import View, DetailView, TemplateView, UpdateView, FormView
from django.contrib.contenttypes.models import ContentType
from asset.forms import DeviceForm, CheckinForm, IpadUpdateForm, AdapterUpdateForm, CaseUpdateForm, HeadphonesUpdateForm, CommentUpdateForm
from asset.models import Device, Ipad, Adapter, Headphones, Case, IpadComment, HeadphonesComment, AdapterComment, CaseComment, Lendee


EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Main View
class AssetHome(TemplateView):
    template_name = 'asset/asset_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = base.forms.BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(AssetHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssetHome, self).get_context_data(**kwargs)
        assets = Headphones.objects.all()
        context['objects1'] = assets
        context['objects2'] = assets
        context['objects3'] = assets
        context['table_objects'] = assets
        #asset_history = []
        #history_count = 0
        #for asset in assets:
            #asset_history.append(asset.history.most_recent())
            #history_count += 1
        #context['asset_history'] = asset_history
        #context['history_count'] = history_count
        #context['active_count'] = Headphones.objects.filter(status__title__icontains='active').count()
        context['all_count'] = Headphones.objects.count()
        return context


## Detail Views
class DeviceDetailView(DetailView):
    '''Generic detail view for devices. '''
    context_object_name = 'device'
    template_name = 'asset/asset_detail.html'

    def get_comments(self, comment_class, **kwargs):
        return comment_class.objects.filter(device__pk=self.get_object().pk)


class IpadDetail(DeviceDetailView):
    """ Detail view for iPads."""

    model = Ipad

    def get_context_data(self, **kwargs):
        context = super(IpadDetail, self).get_context_data(**kwargs)
        context['comments'] = self.get_comments(IpadComment)
        return context


class HeadphonesDetail(DeviceDetailView):
    model = Headphones
    comment_model = HeadphonesComment

    def get_context_data(self, **kwargs):
        context = super(HeadphonesDetail, self).get_context_data(**kwargs)
        context['comments'] = self.get_comments(HeadphonesComment)
        return context


class AdapterDetail(DeviceDetailView):
    model = Adapter

    def get_context_data(self, **kwargs):
        context = super(AdapterDetail, self).get_context_data(**kwargs)
        context['comments'] = self.get_comments(AdapterComment)
        return context


class CaseDetail(DeviceDetailView):
    model = Case

    def get_context_data(self, **kwargs):
        context = super(CaseDetail, self).get_context_data(**kwargs)
        context['comments'] = self.get_comments(CaseComment)
        return context


## Create Views
class DeviceAdd(FormView):
    '''View for adding a device.
    '''
    form_class = DeviceForm
    template_name = 'asset/asset_create.html'
    success_url = reverse_lazy('index')

    def _add_device_type(self, device_class, form):
        '''Saves a new device record of a given class (e.g. Ipad)
        with the attributes submitted in a form.
        '''
        form_data = form.cleaned_data
        device = device_class()
        if form_data['description']:
            device.description = form_data['description']
        if form_data['responsible_party']:
            device.responsible_party = form_data['responsible_party']
        device.make = form_data['make']
        if form_data['serial_number']:
            device.serial_number = form_data['serial_number']
        device.purchased_at = form_data['purchased_at']
        device.save()


    def form_valid(self, form):
        """Create a new device of the selected type.
        """
        form_data = form.cleaned_data
        device_type = form_data['device_type']
        if device_type == 'ipad':
            self._add_device_type(Ipad, form)
        elif device_type == 'headphones':
            self._add_device_type(Headphones, form)
        elif device_type == 'adapter':
            self._add_device_type(Adapter, form)
        else:
            self._add_device_type(Case, form)
        return super(DeviceAdd, self).form_valid(form)

    def get(self, request):
        '''Get request renders form if user has permission to add
        a device. Otherwise, redirects to 403 page.'''
        return super(DeviceAdd, self).get(self, request)
        #if request.user.has_perms('add_device'):
        #else:
            #return redirect('asset:permission_denied')


## Update Views
class DeviceUpdateView(UpdateView):
    '''Generic update view for devices.'''
    template_name = 'asset/asset_update.html'
    context_object_name = 'device'


class IpadUpdate(DeviceUpdateView):
    model = Ipad
    form_class = IpadUpdateForm
    success_url = reverse_lazy('devices:ipads')


class HeadphonesUpdate(DeviceUpdateView):
    model = Headphones
    form_class = HeadphonesUpdateForm
    success_url = reverse_lazy('devices:headphones')


class AdapterUpdate(DeviceUpdateView):
    model = Adapter
    form_class = AdapterUpdateForm
    success_url = reverse_lazy('devices:adapters')


class CaseUpdate(DeviceUpdateView):
    model = Case
    form_class = CaseUpdateForm
    success_url = reverse_lazy('devices:cases') 


## Comment Update Views
class CommentUpdateView(UpdateView):
    '''An abstract CommentEdit View.'''
    template_name = 'asset/edit_comment.html'
    # Must define the comment model to update, like so:
    # model = IpadComment
    form_class = CommentUpdateForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        """On success, redirect to the device's detail page."""
        comment = self.get_object()
        return comment.device_url


class IpadCommentUpdate(CommentUpdateView):

    model = IpadComment


class HeadphonesCommentUpdate(CommentUpdateView):

    model = HeadphonesComment


class AdapterCommentUpdate(CommentUpdateView):

    model = AdapterComment


class CaseCommentUpdate(CommentUpdateView):

    model = CaseComment


## Delete Views
class DeviceDelete(View):
    def post(self, request, pk):
        """Deletes the device with the given pk.
        """
        data = {}
        Device.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully deleted device.')
        data['success'] = True
        json_data = json.dumps(data)
        return HttpResponse(json_data, mimetype="application/json")


## Comment Delete Views
class CommentDeleteView(View):
    '''An abstract CommentDelete View.'''

    def get_comment_class(self):
        """Returns the comment class corresponding to a 
        specific device type. Must be implemented by descendant classes.
        
        Example:
            return IpadComment
        """
        raise NotImplementedError

    def post(self, request, device_id, comment_id):
        response_data = {}
        # Delete the comment
        comment_class = self.get_comment_class()
        comment_class.objects.filter(pk=comment_id).delete()
        # Display a message
        messages.success(request, 'Successfully deleted comment.')
        response_data['success'] = True
        response_data['pk'] = comment_id
        json_data = json.dumps(response_data)
        return HttpResponse(json_data, mimetype='application/json')


class IpadCommentDelete(CommentDeleteView):
    def get_comment_class(self):
        return IpadComment


class HeadphonesCommentDelete(CommentDeleteView):
    def get_comment_class(self):
        return HeadphonesComment


class AdapterCommentDelete(CommentDeleteView):
    def get_comment_class(self):
        return AdapterComment


class CaseCommentDelete(CommentDeleteView):
    def get_comment_class(self):
        return CaseComment


## List Views
class DevicesListView(TemplateView):
    '''Index view for devices. This serves as a list view 
    for all device types.'''
    template_name = 'asset/asset_list.html'

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


