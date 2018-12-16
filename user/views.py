from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import request
from django.db import transaction
from django.shortcuts import redirect
from django.forms.models import modelformset_factory
from user.forms import UserForm, ProfileForm
from entity.forms import AddressForm, TelephoneForm, EmailForm, WebsiteForm
from entity.forms import PersonForm
from entity.models.person import Person
from entity.models.entity import Address, Telephone, Email, Website

# User Views

@login_required
@transaction.atomic
def update_profile(request):
    AddressFormSet = modelformset_factory(Address, form=AddressForm, can_delete=True)
    TelephoneFormSet = modelformset_factory(Telephone, form=TelephoneForm, can_delete=True)
    EmailFormSet = modelformset_factory(Email, form=EmailForm, can_delete=True)
    WebsiteFormSet = modelformset_factory(Website, form=WebsiteForm, can_delete=True)
    
    user = request.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        addr = AddressFormSet(request.POST,request.FILES,queryset=user.profile.address.all(),prefix="addr")
        tel = TelephoneFormSet(request.POST,request.FILES,queryset=user.profile.telephone.all(),prefix="tel")
        email = EmailFormSet(request.POST,request.FILES,queryset=user.profile.email.all(),prefix="email")
        web = WebsiteFormSet(request.POST,request.FILES,queryset=user.profile.website.all(),prefix="web")
        if user_form.is_valid():
            if user:
                user = user_form.save(commit=False)
            else:
                user = user_form.save()
            for a in addr.save():
                user.profile.address.add(a)
            for t in tel.save():
                user.profile.telephone.add(t)
            for e in email.save():
                user.profile.email.add(e)
            for w in web.save():
                user.profile.website.add(w) 
            user_form.save()
            profile_form.save()
            return redirect('user')

    elif user:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        addr = AddressFormSet(queryset=user.profile.address.all(),prefix="addr")
        tel = TelephoneFormSet(queryset=user.profile.telephone.all(),prefix="tel")
        email = EmailFormSet(queryset=user.profile.email.all(),prefix="email")
        web = WebsiteFormSet(queryset=user.profile.website.all(),prefix="web")
        #social = WebsiteFormSet(queryset=person.websites.all(),prefix="social")

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        addr = AddressFormSet(queryset=Address.objects.none(),prefix="addr")
        tel = TelephoneFormSet(queryset=Telephone.objects.none(),prefix="tel")
        email = EmailFormSet(queryset=Email.objects.none(),prefix="email")
        web = WebsiteFormSet(queryset=Website.objects.none(),prefix="web")
        #social = WebsiteFormSet(queryset=Social.objects.none(),prefix="social")
    context = { 'object':user, 'user':user_form, 'profile': profile_form,
              'telephones':tel, 'emails':email, 'websites':web, 'addresses':addr, }

    if user:
        context['title']='Edit %s %s'%(user.first_name,user.last_name)
        context['can_delete']=True

    else:
        context['title']='User Profile'
    return render(request, 'user/profile.html', context)

