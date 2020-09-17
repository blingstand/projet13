#rajouter un ordre dans ma list animals

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
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
        {'name' : 'supprimer',  'id' : 'supprimer', 'function' : 'remove()'}]}
    def get(self, request):
        #get the data from database
        print('-- get --')
        sheets = ut.get_animals_for_template()
        self.context['sheets'] = sheets
        # print(sheets)
        return render(request, 'sheet/index.html', self.context)
    def post(self, request):
        """receives data to pass to deals with the dropSheet function"""
        print('*******')   
        print(request.POST.getlist('checkbox'))
        print('*******')    
        given_id = request.POST.getlist('checkbox')
        print('Avant supression :') #affichage de vérification
        print(f'\t{len(Animal.objects.all())} animaux.')
        print(f'\t{len(AdminData.objects.all())} admin.')
        print(f'\t{len(Owner.objects.all())} owner.')
        ut.drop_sheet(given_id)
        print('Après supression :')
        print(f'\t{len(Animal.objects.all())} animaux.')
        print(f'\t{len(AdminData.objects.all())} admin.')
        print(f'\t{len(Owner.objects.all())} owner.')
        return redirect("sheet:index")
        
class AddSheetView(View): 
    #the add sheet page
    def get(self, request):
        #displays the page
        form = SheetForm()
        owners = Owner.objects.all()
        context = {'form' : form, "owners" : owners}
        return render(request, 'sheet/add.html', context)

    def post(self, request):
        #handles the form and the errors
        form = SheetForm(request.POST)
        print("\n\n***")
        dict_values = {'ask_owner_data':"0", 'mail_id': None}
        dict_values.update(request.POST.dict())
        print("- - - - - ")
        print(dict_values)
        print("- - - - - ")
        if dict_values["ask_owner_data"] == "1":
            selected_owner = Owner.objects.get(id=dict_values["owner_id"])
            print(selected_owner)
            data = {
                "name":selected_owner.owner_name,
                "surname":selected_owner.owner_surname,
                "sex":selected_owner.owner_sex,
                "phone":selected_owner.phone,
                "mail":selected_owner.mail,
                }
            return JsonResponse({"data":data}, safe=False)
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
            print("form not valid")
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
        owners = Owner.objects.all()
        context = {'form' : form, 'animal' : animal,  "owners" : owners}
        return render(request, 'sheet/alter.html', context)

    def post(self, request, given_id):
        """ picks up the data in order to modify the db """
        form = SheetForm(request.POST)
        dict_values = request.POST.dict()
        context = {'form' : form}
        if form.is_valid():
            # print("\t2/ affichage des données récupérées ...")
            print(f">{dict_values}")
            print("---dict_values")
            # print("\t3/ Tentative d'enregistrement des données ...")
            success, response = ut.modify_datas(given_id, dict_values)
            print('---end modify_datas')
            if success:
                print(f'{response} changement(s)')
                context = {'form' : form}
                return redirect("sheet:index")  
            else: 
                context["error"] = response  
                return render(request, 'sheet/alter.html', context)        
        context['error'] = form.errors.items()
        print("\n\n*** E R R O R ***\n")
        print(form.errors.items())
        print("\n*** E N D ***\n\n")
        print(request.POST, 'et', request.FILES)
        return render(request, 'sheet/add.html', context)

