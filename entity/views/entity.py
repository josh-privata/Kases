# Entity Views #

#import vobject

from django.shortcuts import render
#from django.core.urlresolvers import reverse
#from django.forms.formsets import formset_factory
from django.views.generic import TemplateView
from entity.models.person import Person
from entity.models.company import Company
from utils.forms import BootstrapAuthenticationForm


# Entity Main
class EntityHome(TemplateView):
    template_name = 'entity/entity_index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = BootstrapAuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return super(EntityHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EntityHome, self).get_context_data(**kwargs)
        persons = Person.objects.all()
        companies = Company.objects.all()
        entity_history = []
        history_count = 0
        all_company_count = Company.objects.count()
        all_person_count = Person.objects.count()
        counts = {}
        updates = {}
        #for entity in persons:
        #    entity_history.append(entity.history.most_recent())
        #    history_count += 1
        #for entity in companies:
        #    entity_history.append(entity.history.most_recent())
        #    history_count += 1

        # Count Dictionaries
        counts["history"] = {'name':"Entity History",'value':history_count}
        counts["all"] = {'name':"All Companies",'value':all_company_count}
        counts["active"] = {'name':"All People",'value':all_person_count}
        # Updates Dictionaries
        updates["left"] = {'side':"left",
                           'name':"All People",
                           'object_type_plural':'People',
                           'content':persons,
                           'count':all_person_count}
        updates["centre"] = {'side':"centre",
                           'name':"All Companies",
                           'object_type_plural':'Companies',
                           'content':companies,
                           'count':all_company_count}
        updates["right"] = {'side':"right",
                           'name':"History",
                           'object_type_plural':'Entities',
                           'content':entity_history,
                           'count':history_count}
        # Context
        context['counts'] = counts
        context['updates'] = updates
        context['table_objects'] = persons
        context['company_table'] = companies
        return context
