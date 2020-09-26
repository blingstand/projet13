#rajouter un ordre dans ma list animals

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .form import *
from .utils import Utils
from .datas import *

# Create your views here.
ut = Utils()
def redirectIndex(request):
    return redirect('sheet:index')
class SheetView(View):
    #the sheet view page
    context= context_sheet_view
    def get(self, request, own=0):
        #get the data from database
        animals = Animal.objects.all()
        owners = Owner.objects.all()
        # print(owners[0].number_animal())
        self.context['animals'] = animals
        self.context['owners'] = list(owners)
        self.context['disp_owners'] = own 
        print(self.context)
        return render(request, 'sheet/index.html', self.context)
    def post(self, request, own):
        """receives data to pass to deals with the dropSheet function"""
        given_id = request.POST.getlist('checkbox')
        if own == 0: 
            print("demande de suppression pour au moins un animal |", given_id )
            ut.drop_sheet(given_id)
        else: 
            print("demande de suppression pour au moins un humain |", given_id )
            ut.remove_owner(given_id)
        return redirect("sheet:index",own='1')
        
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
        dict_values = {'ask_owner_data':"0"}
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
        print("**////", animal.nature_caution)
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
            successs, response = ut.modify_datas(given_id, dict_values)
            print('---end modify_datas')
            if successs:
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

class AlterOwnerSheetView(View):
    """this class handles get and post for alter_owner page"""
    def get(self, request, given_id, action=None):
        """this function handles get request for alter_owner page"""
        form = SheetForm()
        selected_owner = Owner.objects.get(id=given_id)
        context = {"selected_owner":selected_owner, 'form':form}
        return render(request, "sheet/alter_owner.html", context)
        
    def post(self, request, given_id, action=None):
        """this function handles post request for alter_owner page"""
        print(f"action :", action)
        form = SheetForm()
        context = {'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        if action == "delete":
            success, message = ut.remove_owner(given_id)
            print(success, message)
            if success: 
                return redirect("sheet:index", own=1)
            else: 
                return HttpResponse(message)
        elif action == "modify": 
            success, message = ut.modify_owner(given_id, dict_values)
            if success:
                print(message)
                return redirect("sheet:index", own=1)
            else: 
                context['error'] = message
                print(" * * *")
                print(context)
                print(" * * *")
                return render(request, "sheet/alter_owner.html", context)
        return redirect("sheet:index", own=1)

class AddOwnerSheetView(View):
    """this class handles get and post for alter_owner page"""
    def get(self, request):
        """this function handles the get request for add_owner page"""
        form = SheetForm()
        context = {'form':form}
        return render(request, "sheet/add_owner.html", context)
        
    def post(self, request):
        """this function handles the post request for add_owner page"""
        form = SheetForm()
        context = {'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        print(dict_values)
        if len(dict_values) == 7:
            successs, message = ut.create_owner(dict_values)
            if successs: 
                return redirect("sheet:index", own=1)
            else:
                context['error'] = message
                print(" * * *")
                print(context)
                print(" * * *")
                return render(request, "sheet/add_owner.html", context)
        context['error'] = 'Remplissez tous les champs'
        return render(request, "sheet/add_owner.html", context)


class ContactOwnerView(View): 
    """ this class handles the historic of contact for a given owner """
    def get(self, request, given_id=None): 
        """this method displays historic of contact for a given owner """
        owner = Owner.objects.get(id=given_id)
        contact = owner.contact
        context = {
            'historic_cols':["Date", "Type", "Titre", "Objet"],
            'owner': owner, 'contact': contact, 
            'button_value':[
                {'name' : 'Ajouter Contact',    'id' : 'ajouter', 'function' : 'Add()'}, 
                {'name' : 'Modifier Contact',   'id' : 'modifier', 'function' : 'Alter()'},
                {'name' : 'Supprimer Contact',  'id' : 'supprimer', 'function' : 'Remove()'}]
        }

        return render(request, "sheet/historic.html", context)
    def post(self, request, given_id=None): 
        """this method handles a post request for the  historic of contact page """
        dict_values = request.POST.dict()
        print(f"j'ai reçu {len(dict_values)} données: ", dict_values)
        owner = Owner.objects.get(id=given_id)
        contact = owner.contact
        context = {
            'historic_cols':["Date", "Type", "Titre", "Objet"],
            'owner': owner, 'contact': contact, 
            'button_value':[
                {'name' : 'Ajouter Contact',    'id' : 'ajouter', 'function' : 'Add()'}, 
                {'name' : 'Modifier Contact',   'id' : 'modifier', 'function' : 'Alter()'},
                {'name' : 'Supprimer Contact',  'id' : 'supprimer', 'function' : 'Remove()'}]
        }
        if len(dict_values) == 4: 
            success, message = ut.create_contact(owner, dict_values)
            data = {"success":success, message:"message"}
            return JsonResponse({"data":data}, safe=False)
        return HttpResponse('success ! ', dict_values )
        return render(request, "sheet/historic.html", context)
