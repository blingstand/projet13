#rajouter un ordre dans ma list animals

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .form import *
from .utils import get_animals_for_template
# Create your views here.
class SheetView(View):
    def get(self, request):
        #get the data from database
        animals = get_animals_for_template()
        context={
        'button_value':[
        {'name' : 'trier par',  'id' :'trier'},
        {'name' : 'ajouter',    'id' : 'ajouter'}, 
        {'name' : 'modifier',   'id' : 'modifier'},
        {'name' : 'supprimer',  'id' : 'supprimer'}],
        'animals': animals
        }

        return render(request, 'sheet/index.html', context)

class AddSheetView(View): 
    def get(self, request):
        form = SheetForm()
        context = {'form' : form}
        return render(request, 'sheet/add.html', context)

    def post(self, request):
        form = SheetForm(request.POST, request.FILES)
        print("\n\n***")

        if form.is_valid():
            print("---")
            print("récupération des données,")
            dict_values = form.from_form()
            print("affichage,")
            print(f">{dict_values}")
            print('enregistrement des données')
            form.save_data(dict_values)
            print("\n\n***")
            return HttpResponse("<a href='http://127.0.0.1:8000/spa/admin/sheet/animal/'> animal créé </a>")
        else:
            context = {'form' : form}
            context['errors'] = form.errors.items()
            print("\n\n*** E R R O R ***\n")
            print(form.errors.items())
            print("\n*** E N D ***\n\n")
            print(request.POST, 'et', request.FILES)
            return render(request, 'sheet/add.html', context)