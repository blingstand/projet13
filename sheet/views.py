#rajouter un ordre dans ma list animals

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .form import *
from .utils import Utils

# Create your views here.
ut = Utils()
class SheetView(View):
    #the sheet view page
    context={
    'button_value':[
        {'name' : 'ajouter',    'id' : 'ajouter', 'function' : 'add()'}, 
        {'name' : 'modifier',   'id' : 'modifier', 'function' : 'alter()'},
        {'name' : 'trier par',  'id' :'trier', 'function' : 'classify()'},
        {'name' : 'supprimer',  'id' : 'supprimer', 'function' : 'drop()'}]}
    def get(self, request):
        #get the data from database
        print('-- get --')
        sheets = ut.get_animals_for_template()
        self.context['sheets'] = sheets
        # print(sheets)
        return render(request, 'sheet/index.html', self.context)
    def post(self, request):
        """receives data to pass to deals with the dropSheet function"""
        if request.POST['checkbox']: 

            print('*******')   
            print(request.POST['checkbox'])
            print('*******')    
            given_id = request.POST['checkbox'],
            print(type(given_id))
            print('Avant supression :')
            print(f'\t{len(Animal.objects.all())} animaux.')
            print(f'\t{len(AdminData.objects.all())} admin.')
            print(f'\t{len(Owner.objects.all())} owner.')
            ut.drop_sheet(given_id)
            print('Après supression :')
            print(f'\t{len(Animal.objects.all())} animaux.')
            print(f'\t{len(AdminData.objects.all())} admin.')
            print(f'\t{len(Owner.objects.all())} owner.')
            return redirect("sheet:index")

        return render(request, 'sheet/index.html', self.context)

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
            # print("\t1/ récupération des données ...")
            dict_values = form.from_form()
            # print("\t2/ affichage des données récupérées ...")
            print(f">{dict_values}")
            # print("\t3/ Tentative d'enregistrement des données ...")
            status_operation = form.save_new_datas(dict_values)
            if status_operation == 1:
                print('Réussite')
                # print("\t4/ Fin de la transaction, retour sur la page sheet.")
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
    """ displays the page that can modify the db """
    def get(self, request, given_id):
        """ display informations and form """
        form = SheetForm()
        #I need to get the concerned animal corresponding this given_id
        animal = ut.get_animal_from_given_id(given_id)[0]

        context = {'form' : form, 'animal' : animal}
        return render(request, 'sheet/alter.html', context)

    def post(self, request, given_id):
        """ picks up the data in order to modify the db """
        form = SheetForm(request.POST)
        print("\n\n***")
        if form.is_valid():
            print("---")
            # print("\t1/ récupération des données ...")
            dict_values = form.from_form()
            # print("\t2/ affichage des données récupérées ...")
            print(f">{dict_values}")
            # print("\t3/ Tentative d'enregistrement des données ...")
            status_operation = form.modify_datas(given_id)
            context = {'form' : form}
            return redirect("sheet:index")                
        #         
        else:
            context = {'form' : form}
            context['errors'] = form.errors.items()
            print("\n\n*** E R R O R ***\n")
            print(form.errors.items())
            print("\n*** E N D ***\n\n")
            print(request.POST, 'et', request.FILES)
            return render(request, 'sheet/add.html', context)

