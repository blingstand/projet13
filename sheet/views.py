#rajouter un ordre dans ma list animals

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
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
        sheets = get_animals_for_template()
        context={
        'button_value':[
        {'name' : 'ajouter',    'id' : 'ajouter', 'function' : 'add()'}, 
        {'name' : 'modifier',   'id' : 'modifier', 'function' : 'alter()'},
        {'name' : 'trier par',  'id' :'trier', 'function' : 'classify()'},
        {'name' : 'supprimer',  'id' : 'supprimer', 'function' : 'drop()'}],
        'sheets': sheets
        }
        print(sheets)
        return render(request, 'sheet/index.html', context)

class AddSheetView(View): 
    def get(self, request):
        form = SheetForm()
        context = {'form' : form}
        return render(request, 'sheet/add.html', context)

    def post(self, request):
        form = SheetForm(request.POST)
        print("\n\n***")

        if form.is_valid():
            print("---")
            print("récupération des données,")
            dict_values = form.from_form()
            print("affichage,")
            print(f">{dict_values}")
            print('enregistrement des données')
            status_operation = form.save_data(dict_values)
            if status_operation == 'tout va bien':
                return redirect("sheet:index")
            else:
                error = status_operation
                context = {'form' : form, 'error' : error}
                raise error
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
    def get(self, request):
        form = SheetForm()
        context = {'form' : form}
        return render(request, 'sheet/alter.html', context)