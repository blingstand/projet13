#rajouter un ordre dans ma list animals
#from django 
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
#from current app 
from .models import *
from .form import *
from .utils import UtilsSheet
from .datas import *

#from others app 
from mydashboard.utils import GraphDatas
from mail.utils import UtilsMail
from mail.mail_manager import MailManager
# Create your views here.
 
gradat = GraphDatas()
mm = MailManager()
uts = UtilsSheet()
utm = UtilsMail()

def redirectIndex(request):
    return redirect('sheet:index')
class SheetView(View):
    #the sheet view page
    context= context_sheet_view
    def get(self, request, own=0, action=None, search=0):
        #get the data from database
        print(f"own={own}, action={action}, search={search}")
        animals = Animal.objects.all()
        owners = Owner.objects.all()
        ow = Owner.objects.get(id=35)
        print(ow.owner_name, ow.last_contact)
        if action == "display":  
            list_owners, list_contacted, list_to_contact = gradat.get_list_for_search
            if search == 1:
                owners = list_owners
            if search == 2: 
                owners = list_contacted
            elif search == 3: 
                owners = list_to_contact
        elif action == "search:prop":
            owners = Owner.objects.get(id=search),
        elif action == "search:anim": 
            animals = Animal.objects.get(id=search),
        self.context['animals'] = animals
        self.context['owners'] = list(owners)
        self.context['disp_owners'] = own 
        return render(request, 'sheet/index.html', self.context)
    def post(self, request, own, search=0):
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
        owners = Owner.objects.all()
        cno = uts.get_choice_new_owner(owners)
        form = SheetForm()
        form.fields['select_owner'].widget = forms.Select(choices=cno)
        context = {'form' : form, "owners" : owners}
        return render(request, 'sheet/add.html', context)

    def post(self, request):
        #handles the form and the errors
        owners = Owner.objects.all()
        cno = uts.get_choice_new_owner(owners)
        form = SheetForm(request.POST or None)
        form.fields['select_owner'].widget = forms.Select(choices=cno)
        dict_values = {'ask_owner_data':"0"}
        dict_values.update(request.POST.dict())

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
            print('form is valid')
            # print("\t1/ récupération des données ...")
            dict_values = form.from_form()
            # print("\t2/ affichage des données récupérées ...")
            print(f"dict_values >{dict_values}")
            # print("\t3/ Tentative d'enregistrement des données ...")
            status_operation, animal = form.save_new_datas(dict_values)
            if status_operation == 1:   
                mm.has_to_send_mail('creation', [animal.owner], animal.id)
                print("> un mail a été envoyé suite à cet ajout")
                # print("\t4/ Fin de la transaction, retour sur la page sheet.")
                return redirect("sheet:index")
            else:
                print('Echec, raison :')
                print("***\n\t",status_operation,"\n***")
                context = {'form' : form, "owners" : owners, 'error' : status_operation}                
                return render(request, 'sheet/add.html', context)
        else:
            print("form not valid")
            context = {'form' : form, "owners" : owners}
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
        owners = Owner.objects.all()
        cno = uts.get_choice_new_owner(owners)
        given_values = uts.get_data_for_alter(given_id)
        print("AlterSheetView > ", given_values)
        form = SheetForm(request.POST or None, initial=given_values)
        form.fields['select_owner'].widget = forms.Select(choices=cno)
        #I need to get the concerned animal corresponding this given_id
        animal = uts.get_animal_from_given_id(given_id)[0]
        owners = Owner.objects.all()
        context = {'form' : form, 'animal' : animal,  "owners" : owners}
        return render(request, 'sheet/alter.html', context)

    def post(self, request, given_id):
        """ picks up the data in order to modify the db """
        owners = Owner.objects.all()
        cno = uts.get_choice_new_owner(owners)
        given_values = uts.get_data_for_alter(given_id)
        form = SheetForm(request.POST or None, initial=given_values)
        form.fields['select_owner'].widget = forms.Select(choices=cno)
        dict_values = request.POST.dict()
        context = {'form' : form}
        if form.is_valid():
            print("alter > form is valid")
            print(f"> \t{dict_values}")
            # print("\t3/ Tentative d'enregistrement des données ...")
            success, response = uts.manage_modify_datas(given_id, dict_values)
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
        selected_owner = Owner.objects.get(id=given_id)
        initial_dict = { 
        "owner_name" :  selected_owner.owner_name,
        "owner_surname" :  selected_owner.owner_surname,
        "owner_sex": selected_owner.owner_sex,
        "mail": selected_owner.mail,
        "phone": selected_owner.phone,
        } 
        form = JustOwnerForm(request.POST or None, initial = initial_dict)
        animals = Animal.objects.filter(owner=selected_owner)
        context = {"selected_owner":selected_owner, 'form':form, 'animals':animals}
        print(context)
        return render(request, "sheet/alter_owner.html", context)
        
    def post(self, request, given_id, action=None):
        """this function handles post request for alter_owner page"""
        print(f"action :", action)
        form = JustOwnerForm(request.POST or None)
        selected_owner = Owner.objects.get(id=given_id)
        context = {"selected_owner":selected_owner,'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        if action == "delete":
            success, message = uts.remove_owner(given_id)
            print(success, message)
            if success: 
                return redirect("sheet:index", own=1)
            else: 
                return HttpResponse(message)
        elif action == "modify": 
            success, message = uts.modify_owner(given_id, dict_values)
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
        form = JustOwnerForm()
        context = {'form':form}
        return render(request, "sheet/add_owner.html", context)
        
    def post(self, request):
        """this function handles the post request for add_owner page"""
        form = JustOwnerForm(request.POST)
        print(form.fields)
        context = {'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        print(dict_values)
        if form.is_valid:
            success, message = uts.create_owner(dict_values)
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
            success, message = mm.create_contact(owner, dict_values)
            if success: 
                return JsonResponse({"data":f'{success}{message}'}, safe=False)
            print(message)
        elif action == "remove":
            success, message = uts.remove_contact(request.POST.getlist('id_check[]'))
            print('//////')
            print(success, message)
            print('//////')
            if success: 
                return JsonResponse({"data":f'{success}{message}'}, safe=False)
        elif action == "modify": 
            print(dict_values)
            success, message = uts.modify_contact(dict_values)
            if success: 
                print(message)
                return JsonResponse({"data":f'{success}{message}'}, safe=False)
            print(message)
        return render(request, "sheet/historic.html", self.context)

class AddOwnerOpenSheetView(View):

    def get(self, request):
        """this function handles the get request for add_owner page"""
        print(">>>OPEN add")
        form = JustOwnerForm()
        context = {'form':form}
        return render(request, "sheet/add_owner_open.html", context)
        
        
    def post(self, request):
        """this function handles the post request for add_owner page"""
        print(">>>OPEN add" )
        form = JustOwnerForm(request.POST)
        print(form.fields)
        context = {'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        print(dict_values)
        if form.is_valid:
            success, message = uts.create_owner(dict_values)
            if success: 
                return HttpResponse('<script type="text/javascript">window.close()</script>')  
            else:
                context['error'] = message
                print(" * * *")
                print(context)
                print(" * * *")
                return render(request, "sheet/add_owner_open.html", context)
        context['error'] = 'Remplissez tous les champs'
        return render(request, "sheet/add_owner_open.html", context)

class AlterOwnerOpenSheetView(View): 
    def get(self, request, given_id, action=None):
        """this function handles get request for alter_owner page"""
        print(">>>OPEN alter")
        selected_owner = Owner.objects.get(id=given_id)
        initial_dict = { 
        "owner_name" :  selected_owner.owner_name,
        "owner_surname" :  selected_owner.owner_surname,
        "owner_sex": selected_owner.owner_sex,
        "mail": selected_owner.mail,
        "phone": selected_owner.phone,
        } 
        form = JustOwnerForm(request.POST or None, initial = initial_dict)
        animals = Animal.objects.filter(owner=selected_owner)
        context = {"selected_owner":selected_owner, 'form':form, 'animals':animals}
        print(context)
        return render(request, "sheet/alter_owner_open.html", context)
        
    def post(self, request, given_id, action=None):
        """this function handles post request for alter_owner page"""
        print(">>>OPEN alter")
        print(f"action :", action)
        form = JustOwnerForm(request.POST or None)
        context = {'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        if action == "modify": 
            success, message = uts.modify_owner(given_id, dict_values)
            if success:
                print("1", message)
                return HttpResponse('<script type="text/javascript">window.close()</script>')  
            else: 
                context['error'] = message
                print(" * * *")
                print(context)
                print(" * * *")
                return render(request, "sheet/alter_owner_open.html", context)
        elif action == "delete":
            success, message = uts.remove_owner(given_id)
            print(success, message)
            if success: 
                return HttpResponse('<script type="text/javascript">window.close()</script>')  
            else: 
                return HttpResponse(message)
        return HttpResponse('<script type="text/javascript">window.close()</script>')  