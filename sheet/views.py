#rajouter un ordre dans ma list animals

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .form import *
from .utils import get_animals_for_template, get_animal_from_given_id

# Create your views here.

class SheetView(View):
    #the sheet view page
    def get(self, request):
        #get the data from database
        sheets = get_animals_for_template()
        context={
        'button_value':[
        {'name' : 'ajouter',    'id' : 'ajouter', 'function' : 'add()'}, 
        {'name' : 'modifier',   'id' : 'modifier', 'function' : 'alter()'},
        {'name' : 'trier par',  'id' :'trier', 'function' : 'classify()'},
        {'name' : 'supprimer',  'id' : 'supprimer', 'function' : 'drop()'}],
        'sheets': sheets
        }
        # print(sheets)
        return render(request, 'sheet/index.html', context)

class AddSheetView(View): 
    #the add sheet page
    def get(self, request):
        #displays the page
        form = SheetForm()
        context = {'form' : form}
        return render(request, 'sheet/add.html', context)

    def post(self, request):
        #handles the form and the errors
        form = SheetForm(request.POST)
        print("\n\n***")

        if form.is_valid():
            print("---")
            print("\t1/ récupération des données ...")
            dict_values = form.from_form()
            print("\t2/ affichage des données récupérées ...")
            print(f">{dict_values}")
            print("\t3/ Tentative d'enregistrement des données ...")
            status_operation = form.save_data(dict_values)
            if status_operation == 1:
                print('Réussite')
                print("\t4/ Fin de la transaction, retour sur la page sheet.")
                return redirect("sheet:index")
            else:
                print('\tEchec, raison :')
                print("***\n",status_operation,"\n***")
                context = {'form' : form, 'error' : status_operation}
                
                return render(request, 'sheet/add.html', context)
        else:
            context = {'form' : form}
            context['errors'] = form.errors.items()
            print("\n\n*** E R R O R ***\n")
            print(form.errors.items())
            print("\n*** E N D ***\n\n")
            print(request.POST, 'et', request.FILES)
            return render(request, 'sheet/add.html', context)

class AlterSheetView(View): 
    #the sheet alter page
    def get(self, request, given_id):
        form = SheetForm()
        #I need to get the concerned animal corresponding this given_id
        animal = get_animal_from_given_id(given_id)[0]
        print(">>>", animal.race)
        context = {'form' : form, 'animal' : animal}
        return render(request, 'sheet/alter.html', context)