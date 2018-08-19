# Person Views #

#import vobject
import re
from django import http
from django.shortcuts import render_to_response, render
#from django.core.urlresolvers import reverse
#from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.contrib.sitemaps import Sitemap
from entity.forms import AddressForm, TelephoneForm, EmailForm, WebsiteForm
from entity.forms import PersonForm, SearchForm, AdvancedSearchForm
from entity.models.person import Person
from entity.models.entity import Address, Telephone, Email, Website


# Helper Classes
class ListWrapper:
    def __init__(self,lst):
        self._list = lst
    def count(self):
        return len(self._list)
    def __getitem__(self,i):
        return self._list[i]
      

class AddressbookSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Person.objects.all()

    def lastmod(self, obj):
        return obj.modified


def find_person(request,lastname,firstname):
    try:
        person = Person.objects.get(slug_last__iexact=lastname,slug_first__iexact=firstname)
        return ListWrapper([person])
    except Person.DoesNotExist:
        qs = Person.objects.filter(last_name__istartswith=lastname, first_name__istartswith=firstname)
        if qs.count()>0:
            return qs
        qs = Person.objects.filter(last_name__istartswith=lastname)
        return qs


def index(request):

    """
    <form action="" method="post">
    <table>
    {% ifequal mode "advanced" %}
    {{form}}
    <tr><td><a href="#">Simple Search</a></td>
    <td><input type="submit" name="submit" value="Search" /></td></tr>
    {% else %}
    <tr><td>{{form.first}}</td><td>{{form.last}}</td>
    <td><input type="submit" name="submit" value="Search" /></td></tr>
    <tr><td>{{form.first.label_tag}}</td><td>{{form.last.label_tag}}</td>
    <td><a href="#">Advanced Search</a></td></tr>
    <tr><td colspan="2" /><td><a href="?new=1">Add New Person</a></td></tr>
    {% endifequal %}
    </table>
    </form>
    """
    if request.GET.get('new', False):
        return person_edit(request)
    #return person_search(request,None)
    mode = request.GET.get('mode', 'normal')
    mode = mode.lower()
    if request.method == 'POST':
        if mode=='advanced':
            form = AdvancedSearchForm(request.POST,request.FILES)
        else:
            form = SearchForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            qs = Person.objects
            all = True
            fields = [ ('first','first_name__istartswith'),
                      ('last','last_name__istartswith'),
                      ('line1', 'addresses__line1__icontains'),
                      ('line2', 'addresses__line2__icontains'),
                      ('line3', 'addresses__line3__icontains'),
                      ('city', 'addresses__city__icontains'),
                      ('state', 'addresses__state__icontains'),
                      ('postcode', 'addresses__postcode__icontains'),
                      ('country', 'addresses__state__country__title__icontains'),
                      ('phone', 'telephones__number__contains' ),
                      ('email', 'emails__email__icontains'),
                      ('website','websites__url__icontains'),
                       ]
            for name,query in fields:
                try:
                    if data[name] and re.match('[a-zA-Z0-9]+',data[name]):
                        qs = eval('qs.filter('+query+'="'+data[name]+'")')
                        all = False
                except KeyError:
                    pass
            if data['has_phone']:
                all = False
                qs = qs.filter(telephones__number__regex=r'[0-9]+')
                #data['has_phone'] = not data['has_phone']
            if all:
                qs = qs.all()
            return do_person_search(request,qs)
    else:
        if mode=='advanced':
            form = AdvancedSearchForm()
        else:
            form = SearchForm()
    context = {'form':form, 'mode':mode, 'title':'Our Address Book'}
    return render_to_response('entity/person/person_index.html',context)


def person_search(request,query):
    if query:
        qs = Person.objects.filter(last_name__istartswith=query)
    else:
        qs = Person.objects.all()
    return do_person_search(request, qs)
 

def person_by_name(request,lastname,firstname):
    qs = find_person(request,lastname,firstname)
    if not qs:
        raise http.Http404
    person = qs[0]
    context = { 'object':person,
               'title':'%s %s'%(person.first_name,person.last_name),
               'is_popup':request.GET.get('print',False) }
    return render(request, 'entity/person/person_detail.html', context)


def person_detail(request, object_id=None):
    if object_id:
        try:
            person = Person.objects.get(pk=object_id)
            context = { 'object':person,
            'title':'%s %s'%(person.first_name,person.last_name),
            'is_popup':request.GET.get('print',False) }
            return render(request, 'entity/person/person_detail.html', context)
        except Person.DoesNotExist:
            raise http.Http404


def person_add(request):
    AddressFormSet = modelformset_factory(Address, form=AddressForm, can_delete=True)
    TelephoneFormSet = modelformset_factory(Telephone, form=TelephoneForm, can_delete=True)
    EmailFormSet = modelformset_factory(Email, form=EmailForm, can_delete=True)
    WebsiteFormSet = modelformset_factory(Website, form=WebsiteForm, can_delete=True)
    #SocialFormSet = modelformset_factory(Social, form=SocialForm, can_delete=True)
    person = None   
    if request.method == 'POST':
        #if request.POST.has_key('cancel'):
        #    return http.HttpResponseRedirect("..")
        #if request.POST.has_key('delete'):
        #    if object_id:
        #        return http.HttpResponseRedirect(reverse('entity.views.person_delete',args=[person.slug_last,person.slug_first]))
        #    else:
        #        return http.HttpResponseRedirect(reverse('entity.views.person_delete',args=[lastname,firstname]))
        form = PersonForm(request.POST,request.FILES,prefix="person")
        addr = AddressFormSet(request.POST,request.FILES,queryset=Address.objects.none(),prefix="addr")
        tel = TelephoneFormSet(request.POST,request.FILES,queryset=Telephone.objects.none(),prefix="tel")
        email = EmailFormSet(request.POST,request.FILES,queryset=Email.objects.none(),prefix="email")
        web = WebsiteFormSet(request.POST,request.FILES,queryset=Website.objects.none(),prefix="web")
        #social = SocialFormSet(request.POST,request.FILES,queryset=Social.objects.none(),prefix="social")
        if form.is_valid() and addr.is_valid() and tel.is_valid() and email.is_valid() and web.is_valid():
            person = form.save()
            for a in addr.save():
                person.address.add(a)
            for t in tel.save():
                person.telephone.add(t)
            for e in email.save():
                person.email.add(e)
            for w in web.save():
                person.website.add(w) 
            person.save()
            return http.HttpResponseRedirect(person.get_absolute_url())      
    form = PersonForm(prefix="person")
    addr = AddressFormSet(queryset=Address.objects.none(),prefix="addr")
    tel = TelephoneFormSet(queryset=Telephone.objects.none(),prefix="tel")
    email = EmailFormSet(queryset=Email.objects.none(),prefix="email")
    web = WebsiteFormSet(queryset=Website.objects.none(),prefix="web")
    #social = WebsiteFormSet(queryset=Social.objects.none(),prefix="social")
    context = { 'object':person, 'person':form, 'telephones':tel, 'emails':email,
               'websites':web, 'addresses':addr, }
    context['title']='New Addressbook Entry'
    return render(request, 'entity/person/person_create.html', context)


def person_update(request, object_id=None):
    AddressFormSet = modelformset_factory(Address, form=AddressForm, can_delete=True)
    TelephoneFormSet = modelformset_factory(Telephone, form=TelephoneForm, can_delete=True)
    EmailFormSet = modelformset_factory(Email, form=EmailForm, can_delete=True)
    WebsiteFormSet = modelformset_factory(Website, form=WebsiteForm, can_delete=True)
    #SocialFormSet = modelformset_factory(Social, form=SocialForm, can_delete=True)
    if object_id:
        try:
            person = Person.objects.get(pk=object_id)
        except Person.DoesNotExist:
            raise http.Http404
    elif firstname and lastname:
        qs = find_person(request,lastname,firstname)
        if qs.count()>1:
            return http.HttpResponseRedirect(reverse('entity.views.personsearch',args=[lastname]))
        person = qs[0]
    else:
        person = None
    if request.method == 'POST':
        #if request.POST.has_key('cancel'):
        #    return http.HttpResponseRedirect("..")
        #if request.POST.has_key('delete'):
        #    if object_id:
        #        return http.HttpResponseRedirect(reverse('entity.views.person_delete',args=[person.slug_last,person.slug_first]))
        #    else:
        #        return http.HttpResponseRedirect(reverse('entity.views.person_delete',args=[lastname,firstname]))
        if person:        
            form = PersonForm(request.POST,request.FILES,instance=person,prefix="person")
            addr = AddressFormSet(request.POST,request.FILES,queryset=person.address.all(),prefix="addr")
            tel = TelephoneFormSet(request.POST,request.FILES,queryset=person.telephone.all(),prefix="tel")
            email = EmailFormSet(request.POST,request.FILES,queryset=person.email.all(),prefix="email")
            web = WebsiteFormSet(request.POST,request.FILES,queryset=person.website.all(),prefix="web")
            #social = SocialFormSet(request.POST,request.FILES,queryset=person.social.all(),prefix="social")
        else:
            form = PersonForm(request.POST,request.FILES,prefix="person")
            addr = AddressFormSet(request.POST,request.FILES,queryset=Address.objects.none(),prefix="addr")
            tel = TelephoneFormSet(request.POST,request.FILES,queryset=Telephone.objects.none(),prefix="tel")
            email = EmailFormSet(request.POST,request.FILES,queryset=Email.objects.none(),prefix="email")
            web = WebsiteFormSet(request.POST,request.FILES,queryset=Website.objects.none(),prefix="web")
            #social = SocialFormSet(request.POST,request.FILES,queryset=Social.objects.none(),prefix="social")
        if form.is_valid() and addr.is_valid() and tel.is_valid() and email.is_valid() and web.is_valid():
            if person:
                person = form.save(commit=False)
            else:
                person = form.save()
            for a in addr.save():
                person.address.add(a)
            for t in tel.save():
                person.telephone.add(t)
            for e in email.save():
                person.email.add(e)
            for w in web.save():
                person.website.add(w) 
            #for s in social.save():
            #    person.social.add(w) 
            person.save()
            return http.HttpResponseRedirect(person.get_absolute_url())       
    elif person:
        form = PersonForm(instance=person,prefix="person")
        addr = AddressFormSet(queryset=person.address.all(),prefix="addr")
        tel = TelephoneFormSet(queryset=person.telephone.all(),prefix="tel")
        email = EmailFormSet(queryset=person.email.all(),prefix="email")
        web = WebsiteFormSet(queryset=person.website.all(),prefix="web")
        #social = WebsiteFormSet(queryset=person.websites.all(),prefix="social")
    else:
        form = PersonForm(prefix="person")
        addr = AddressFormSet(queryset=Address.objects.none(),prefix="addr")
        tel = TelephoneFormSet(queryset=Telephone.objects.none(),prefix="tel")
        email = EmailFormSet(queryset=Email.objects.none(),prefix="email")
        web = WebsiteFormSet(queryset=Website.objects.none(),prefix="web")
        #social = WebsiteFormSet(queryset=Social.objects.none(),prefix="social")
    context = { 'object':person, 'person':form, 'telephones':tel, 'emails':email,
               'websites':web, 'addresses':addr, }
    if person:
        context['title']='Edit %s %s'%(person.first_name,person.last_name)
        context['can_delete']=True
    else:
        context['title']='New Addressbook Entry'
    return render(request, 'entity/person/person_update.html', context)


def person_delete(request, object_id=None):
    person = person_detail(request, object_id)
    del person
    if request.method == 'POST':
        if request.POST.has_key('cancel'):
            return http.HttpResponseRedirect(reverse('entity.views.person_detail',args=[object_id]))
        for a in list(object.address.all())+list(object.telephone.all())+list(object.email.all())+list(object.website.all()):
            a.delete()
        object.delete()
        return http.HttpResponseRedirect(reverse('entity.views.index'))
    return render_to_response('entity/person/person_delete.html',locals())


#def vcard_export(request):
#    filename = 'addresses'
#    if request.method == 'POST':
#        form = ExportForm(request.POST,request.FILES)
#        if form.is_valid():
#            data = form.cleaned_data
#            qs = Person.objects.filter(pk__in=data['ids'].split(','))
#            result = []
#            for person in qs:
#                print(person)
#                vc = vobject.vCard()
#                vc.add('n')
#                vc.n.value = vobject.vcard.Name(family=person.last_name, given=person.first_name)
#                vc.add('fn')
#                vc.fn.value = ' '.join([person.first_name,person.last_name])
#                for email in person.emails.all():
#                    obj = vc.add('email')
#                    obj.value = email.email
#                    obj.type_param = email.location.value
#                for tel in person.telephones.all():
#                    obj = vc.add('tel')
#                    obj.value = tel.number
#                    obj.type_param = ','.join([tel.location.value,tel.get_type_display()])
#                for addr in person.addresses.all():
#                    obj = vc.add('adr')
#                    street = ''
#                    if addr.line1:
#                        street = [addr.line1]
#                    if addr.line2:
#                        street.append(addr.line2)
#                    if addr.line3:
#                        street.append(addr.line3)
#                    region=addr.state.long_name if addr.state else ''
#                    country=addr.state.country.name if addr.state else ''
#                    obj.value = vobject.vcard.Address(street=street, city=addr.city, region=region, country=country, code=addr.postcode)
#                    obj.type_param = addr.location.value
#                if person.image:
#                    obj = vc.add('photo')
#                    obj.value = person.image
#                    obj.value_param='URL'
#                vc.add('rev').value = person.modified.isoformat()
#                result.append(vc.serialize())
#            if len(result)==1:
#                filename = '_'.join([qs[0].first_name, qs[0].last_name])
#            else:
#                filename += '-'+datetime.datetime.now().date().isoformat()
#            resp = http.HttpResponse('\n\n'.join(result),content_type='text/vcard')
#            resp['Content-Disposition'] = 'attachment; filename="'+filename+'.vcf"'
#            return resp
#    raise http.Http404
 


#def do_person_search(request,queryset):
#    def get_url(object):
#        e = object.primary_email()
#        if e:
#            return e.url()
#        return None
    
#    table = Table( [ TableColumn('First Name','first_name',url=True, clazz="name"),
#                    TableColumn('Last Name','last_name',url=True, clazz="name"),
#                    TableColumn('Address','primary_address()',sort=False,url=False, clazz="address"),
#                    TableColumn('Telephone','primary_telephone()',sort=False,url=False),
#                    TableColumn('Email','primary_email()',sort=False, 
#                                url=get_url),
#                    ],
#                    context={'title':'Our Address Book', 'table_class':'addressbook'},
#                    default='last_name'
#                    )
#    table.paginate(request,queryset)
#    table.context['export_form'] = ExportForm({ 'ids':','.join([str(qs.pk) for qs in queryset]) })
#    return render_to_response('entity/person/person_list.html',table.context,context_instance=RequestContext(request))
   
