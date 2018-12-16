# Company Views #

#import vobject
import re
from django import http
from django.shortcuts import render_to_response
from django.shortcuts import render
#from django.core.urlresolvers import reverse
#from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.contrib.sitemaps import Sitemap
from entity.forms import AddressForm
from entity.forms import  TelephoneForm
from entity.forms import EmailForm
from entity.forms import  WebsiteForm
from entity.forms import CompanyForm
from entity.forms import SocialForm
from entity.models.company import Company
from entity.models.entity import Address
from entity.models.entity import Telephone
from entity.models.entity import Email
from entity.models.entity import Website
from entity.models.entity import Social


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
		return Company.objects.all()

	def lastmod(self, obj):
		return obj.modified


def find_company(request,lastname,firstname):
	try:
		company = Company.objects.get(slug_last__iexact=lastname,slug_first__iexact=firstname)
		return ListWrapper([company])
	except Company.DoesNotExist:
		qs = Company.objects.filter(last_name__istartswith=lastname, first_name__istartswith=firstname)
		if qs.count()>0:
			return qs
		qs = Company.objects.filter(last_name__istartswith=lastname)
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
	<tr><td colspan="2" /><td><a href="?new=1">Add New Company</a></td></tr>
	{% endifequal %}
	</table>
	</form>
	"""
	if request.GET.get('new', False):
		return company_edit(request)
	#return company_search(request,None)
	mode = request.GET.get('mode', 'normal')
	mode = mode.lower()
	if request.method == 'POST':
		if mode=='advanced':
			form = AdvancedSearchForm(request.POST,request.FILES)
		else:
			form = SearchForm(request.POST,request.FILES)
		if form.is_valid():
			data = form.cleaned_data
			qs = Company.objects
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
			return do_company_search(request,qs)
	else:
		if mode=='advanced':
			form = AdvancedSearchForm()
		else:
			form = SearchForm()
	context = {'form':form, 'mode':mode, 'title':'Our Address Book'}
	return render_to_response('entity/company/company_index.html',context)


def company_search(request,query):
	if query:
		qs = Company.objects.filter(title__istartswith=query)
	else:
		qs = Company.objects.all()
	return do_company_search(request, qs)


def company_add(request):
	AddressFormSet = modelformset_factory(Address, form=AddressForm, can_delete=True)
	TelephoneFormSet = modelformset_factory(Telephone, form=TelephoneForm, can_delete=True)
	EmailFormSet = modelformset_factory(Email, form=EmailForm, can_delete=True)
	WebsiteFormSet = modelformset_factory(Website, form=WebsiteForm, can_delete=True)
	SocialFormSet = modelformset_factory(Social, form=SocialForm, can_delete=True)
	company = None   
	if request.method == 'POST':
		#if request.POST.has_key('cancel'):
		#    return http.HttpResponseRedirect("..")
		#if request.POST.has_key('delete'):
		#    if object_id:
		#        return http.HttpResponseRedirect(reverse('entity.views.company_delete',args=[company.slug_last,company.slug_first]))
		#    else:
		#        return http.HttpResponseRedirect(reverse('entity.views.company_delete',args=[lastname,firstname]))
		form = CompanyForm(request.POST,request.FILES,prefix="company")
		addr = AddressFormSet(request.POST,request.FILES,queryset=Address.objects.none(),prefix="addr")
		tel = TelephoneFormSet(request.POST,request.FILES,queryset=Telephone.objects.none(),prefix="tel")
		email = EmailFormSet(request.POST,request.FILES,queryset=Email.objects.none(),prefix="email")
		web = WebsiteFormSet(request.POST,request.FILES,queryset=Website.objects.none(),prefix="web")
		social = SocialFormSet(request.POST,request.FILES,queryset=Social.objects.none(),prefix="social")
		if form.is_valid() and addr.is_valid() and tel.is_valid() and email.is_valid() and web.is_valid() and social.is_valid():
			company = form.save()
			for a in addr.save():
				company.address.add(a)
			for t in tel.save():
				company.telephone.add(t)
			for e in email.save():
				company.email.add(e)
			for w in web.save():
				company.website.add(w) 
			for s in social.save():
				company.social.add(s)
			company.save()
			return http.HttpResponseRedirect(company.get_absolute_url())      
	form = CompanyForm(prefix="company")
	addr = AddressFormSet(queryset=Address.objects.none(),prefix="addr")
	tel = TelephoneFormSet(queryset=Telephone.objects.none(),prefix="tel")
	email = EmailFormSet(queryset=Email.objects.none(),prefix="email")
	web = WebsiteFormSet(queryset=Website.objects.none(),prefix="web")
	social = WebsiteFormSet(queryset=Social.objects.none(),prefix="social")
	context = { 'object':company, 'company':form, 'telephones':tel, 'emails':email,
			   'websites':web, 'socials':social, 'addresses':addr, }
	context['title']='New Addressbook Entry'
	return render(request, 'entity/company/company_create.html', context)


def company_edit(request, object_id=None):
	AddressFormSet = modelformset_factory(Address, form=AddressForm, can_delete=True)
	TelephoneFormSet = modelformset_factory(Telephone, form=TelephoneForm, can_delete=True)
	EmailFormSet = modelformset_factory(Email, form=EmailForm, can_delete=True)
	WebsiteFormSet = modelformset_factory(Website, form=WebsiteForm, can_delete=True)
	SocialFormSet = modelformset_factory(Social, form=SocialForm, can_delete=True)
	if object_id:
		try:
			company = Company.objects.get(pk=object_id)
		except Company.DoesNotExist:
			raise http.Http404
	elif firstname and lastname:
		qs = find_company(request,lastname,firstname)
		if qs.count()>1:
			return http.HttpResponseRedirect(reverse('entity.views.companysearch',args=[lastname]))
		company = qs[0]
	else:
		company = None
	if request.method == 'POST':
		#if request.POST.has_key('cancel'):
		#    return http.HttpResponseRedirect("..")
		#if request.POST.has_key('delete'):
		#    if object_id:
		#        return http.HttpResponseRedirect(reverse('entity.views.company_delete',args=[company.slug_last,company.slug_first]))
		#    else:
		#        return http.HttpResponseRedirect(reverse('entity.views.company_delete',args=[lastname,firstname]))
		if company:        
			form = CompanyForm(request.POST,request.FILES,instance=company,prefix="company")
			addr = AddressFormSet(request.POST,request.FILES,queryset=company.address.all(),prefix="addr")
			tel = TelephoneFormSet(request.POST,request.FILES,queryset=company.telephone.all(),prefix="tel")
			email = EmailFormSet(request.POST,request.FILES,queryset=company.email.all(),prefix="email")
			web = WebsiteFormSet(request.POST,request.FILES,queryset=company.website.all(),prefix="web")
			social = SocialFormSet(request.POST,request.FILES,queryset=company.social.all(),prefix="social")
		else:
			form = CompanyForm(request.POST,request.FILES,prefix="company")
			addr = AddressFormSet(request.POST,request.FILES,queryset=Address.objects.none(),prefix="addr")
			tel = TelephoneFormSet(request.POST,request.FILES,queryset=Telephone.objects.none(),prefix="tel")
			email = EmailFormSet(request.POST,request.FILES,queryset=Email.objects.none(),prefix="email")
			web = WebsiteFormSet(request.POST,request.FILES,queryset=Website.objects.none(),prefix="web")
			social = SocialFormSet(request.POST,request.FILES,queryset=Social.objects.none(),prefix="social")
		if form.is_valid() and addr.is_valid() and tel.is_valid() and email.is_valid() and web.is_valid() and social.is_valid():
			if company:
				company = form.save(commit=False)
			else:
				company = form.save()
			for a in addr.save():
				company.address.add(a)
			for t in tel.save():
				company.telephone.add(t)
			for e in email.save():
				company.email.add(e)
			for w in web.save():
				company.website.add(w) 
			for s in social.save():
			    company.social.add(s) 
			company.save()
			return http.HttpResponseRedirect(company.get_absolute_url())       
	elif company:
		form = CompanyForm(instance=company,prefix="company")
		addr = AddressFormSet(queryset=company.address.all(),prefix="addr")
		tel = TelephoneFormSet(queryset=company.telephone.all(),prefix="tel")
		email = EmailFormSet(queryset=company.email.all(),prefix="email")
		web = WebsiteFormSet(queryset=company.website.all(),prefix="web")
		social = WebsiteFormSet(queryset=company.websites.all(),prefix="social")
	else:
		form = CompanyForm(prefix="company")
		addr = AddressFormSet(queryset=Address.objects.none(),prefix="addr")
		tel = TelephoneFormSet(queryset=Telephone.objects.none(),prefix="tel")
		email = EmailFormSet(queryset=Email.objects.none(),prefix="email")
		web = WebsiteFormSet(queryset=Website.objects.none(),prefix="web")
		social = WebsiteFormSet(queryset=Social.objects.none(),prefix="social")
	context = { 'object':company, 'company':form, 'telephones':tel, 'emails':email,
			   'websites':web, 'socials':social, 'addresses':addr, }
	if company:
		context['title']='Edit %s' % (company.title)
		context['can_delete']=True
	else:
		context['title']='New Addressbook Entry'
	return render(request, 'entity/company/company_update.html', context)


def company_delete(request, object_id=None):
	company = company_detail(request, object_id)
	del company
	if request.method == 'POST':
		if request.POST.has_key('cancel'):
			return http.HttpResponseRedirect(reverse('entity.views.company_detail',args=[object_id]))
		for a in list(object.addresses.all())+list(object.telephones.all())+list(object.emails.all())+list(object.websites.all()):
			a.delete()
		object.delete()
		return http.HttpResponseRedirect(reverse('entity.views.index'))
	return render_to_response('entity/company/company_delete.html',locals())


def company_detail(request, object_id=None):
	if object_id:
		try:
			company = Company.objects.get(pk=object_id)
			context = { 'object':company,
			'title':'%s'%(company.title),
			'is_popup':request.GET.get('print',False) }
			return render(request, 'entity/company/company_detail.html', context)
		except Company.DoesNotExist:
			raise http.Http404

#def vcard_export(request):
#    filename = 'addresses'
#    if request.method == 'POST':
#        form = ExportForm(request.POST,request.FILES)
#        if form.is_valid():
#            data = form.cleaned_data
#            qs = Company.objects.filter(pk__in=data['ids'].split(','))
#            result = []
#            for company in qs:
#                print(company)
#                vc = vobject.vCard()
#                vc.add('n')
#                vc.n.value = vobject.vcard.Name(family=company.last_name, given=company.first_name)
#                vc.add('fn')
#                vc.fn.value = ' '.join([company.first_name,company.last_name])
#                for email in company.emails.all():
#                    obj = vc.add('email')
#                    obj.value = email.email
#                    obj.type_param = email.location.value
#                for tel in company.telephones.all():
#                    obj = vc.add('tel')
#                    obj.value = tel.number
#                    obj.type_param = ','.join([tel.location.value,tel.get_type_display()])
#                for addr in company.addresses.all():
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
#                if company.image:
#                    obj = vc.add('photo')
#                    obj.value = company.image
#                    obj.value_param='URL'
#                vc.add('rev').value = company.modified.isoformat()
#                result.append(vc.serialize())
#            if len(result)==1:
#                filename = '_'.join([qs[0].first_name, qs[0].last_name])
#            else:
#                filename += '-'+datetime.datetime.now().date().isoformat()
#            resp = http.HttpResponse('\n\n'.join(result),content_type='text/vcard')
#            resp['Content-Disposition'] = 'attachment; filename="'+filename+'.vcf"'
#            return resp
#    raise http.Http404



#def do_company_search(request,queryset):
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
#    return render_to_response('entity/company/company_list.html',table.context,context_instance=RequestContext(request))