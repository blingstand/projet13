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

class AlterOwnerSheetView(View):
    """this class handles get and post for alter_owner page"""
    def get(self, request, given_id, action=None):
        """this function handles get request for alter_owner page"""
        form = SheetForm()
        selected_owner = Owner.objects.get(id=given_id)
        animals = Animal.objects.filter(owner=selected_owner)
        context = {"selected_owner":selected_owner, 'form':form, 'animals':animals}
        print(context)
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
            success, message = ut.create_owner(dict_values)
            if success: 
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
    context = context_contact_owner_view
    def get(self, request, given_id=None, action=None): 
        """this method displays historic of contact for a given owner """
        owner = Owner.objects.get(id=given_id)
        contacts = Contact.objects.filter(owner=owner)
        self.context["owner"] = owner
        self.context["contacts"] = contacts
        return render(request, "sheet/historic.html", self.context)

    def post(self, request, given_id=None, action=None): 
        """this method handles a post request for the  historic of contact page """
        
        print(request.POST.getlist('id_check[]'))
        print("\t>Je reçois une demande de type : ", action)
        dict_values = request.POST.dict()
        # print(f"t>Je  reçois {len(dict_values)} données: ", dict_values)
        owner = Owner.objects.get(id=given_id)
        contacts = Contact.objects.filter(owner=owner)
        self.context["owner"] = owner
        self.context["contacts"] = contacts 
        if action == "add": 
            success, message = ut.create_contact(owner, dict_values)
            if success: 
                return JsonResponse({"data":f'{success}{message}'}, safe=False)
            print(message)
        elif action == "remove":
            success, message = ut.remove_contact(request.POST.getlist('id_check[]'))
            print('//////')
            print(success, message)
            print('//////')
            if success: 
                return JsonResponse({"data":f'{success}{message}'}, safe=False)
        elif action == "modify": 
            print(dict_values)
            success, message = ut.modify_contact(dict_values)
            if success: 
                print(message)
                return JsonResponse({"data":f'{success}{message}'}, safe=False)
            print(message)
        return render(request, "sheet/historic.html", self.context)
