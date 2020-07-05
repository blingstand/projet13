from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *

# Create your views here.
class SheetView(View):
    def get(self, request):
        #get the data from database
        list_animals = [animal for animal in Animal.objects.all()]
        animals = []
        for a in list_animals:
            if a.is_male:
                if a.is_cat: 
                    a.nature = "chat"
                else:
                    a.nature = "chien"
            else:
                if a.is_cat:
                    a.nature = "chatte"
                else:
                    a.nature = "chienne"
            if a.admin_data_id.is_neutered:
                a.status = 'stérile'
            else:
                if a.admin_data_id.can_be_neutered:
                    a.status = f'peut être stérilisé(e)'
                else: 
                    a.status = f'ne peut pas encore être stérilisé(e)'
            if a.owner_id.nb_mail_send > 2:
                a.owner_status = "oui"
            else:
                a.owner_status = "non"
            a.owner = f"{a.owner_id.name.upper()} - {a.owner_id.surname.upper()}"
            print(f"--\n> nom : {a.name}\nnature {a.nature}\nstatut : {a.status}"\
                f"\nrace : {a.race}\npropriétaire : {a.owner}\nstatut propriétaire : {a.owner_status}"\
                f"\ntel propriétaire : {a.owner_id.telephone}"\
                f"\nnum dossier : {a.admin_data_id.file}"\
                f"\nnum tatouage : {a.admin_data_id.tatoo}"\
                f"\nnum puce : {a.admin_data_id.chip}")
            animals.append(a)
        print([animal.owner for animal in animals])
        context={
        'button_value':['trier par', 'ajouter', 'modifier', 'supprimer'],
        'animals': animals
        }

        return render(request, 'sheet/index.html', context)