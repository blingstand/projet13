#rajouter un ordre dans ma list animals
#from django

from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

#from others app
from mydashboard.utils import GraphDatas
from mail.mail_manager import MailManager

#from current app
from .models import Animal, Owner, Contact
from .form import SheetForm, JustOwnerForm
from .utils import UtilsSheet
from .datas import *

# Create your views here.

gradat = GraphDatas()
mail_manager = MailManager()
utils_sheet = UtilsSheet()

def redirect_index(request):
    return redirect('sheet:index')
class SheetView(View):
    """class for page index sheet"""
    
    def get(self, request, own=0, action=None, search=0):
        #get the data from database
        print(f"get own={own}, action={action}, search={search}")
        animals = Animal.objects.all()
        owners = Owner.objects.all()
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
        context = {
            'animals' : animals, 'owners': list(owners), 'disp_owners': own, 
            'top_columns_anim': top_columns_anim, 'top_columns_owner': top_columns_owner, 
            'button_value': button_value
            }
        return render(request, 'sheet/index.html', context)

    def post(self, request, own, search=0):
        """receives data to pass to deals with the dropSheet function"""
        given_id = request.POST.getlist('checkbox')
        print("***************")
        print(given_id, own)

        if own == 0:
            utils_sheet.drop_sheet(given_id)
            return redirect("sheet:index",own='0')

        print("***************")
        utils_sheet.remove_owner(given_id)
        return redirect("sheet:index",own='1')

class AddSheetView(View):
    """class for page add sheet"""
    context = {'title': "Page Ajout Fiche", 'submit_btn': "Ajouter"}
    def get(self, request):
        #displays the page
        owners = Owner.objects.all()
        form = SheetForm(request.POST or None)
        self.context.update({'form' : form, "owners" : owners})
        return render(request, 'sheet/form_anim.html', self.context)

    def post(self, request):
        #handles the form and the errors
        owners = Owner.objects.all()
        form = SheetForm(request.POST or None)
        ajax_search_owner_data = {"value": ""}
        dict_values = request.POST.dict()
        ajax_search_owner_data.update(dict_values)
        self.context.update({'form' : form, "owners" : owners})
        print(ajax_search_owner_data)
        if ajax_search_owner_data['value'] is not "":
            print(">> ", ajax_search_owner_data)
            response = utils_sheet.search_owner(ajax_search_owner_data)
            return JsonResponse({"data":response}, safe=False)
    
        if form.is_valid():
            print('form is valid')
            # print("\t1/ récupération des données ...")
            dict_values = form.from_form()
            # print("\t2/ affichage des données récupérées ...")
            print(f"dict_values >{dict_values}")
            # print("\t3/ Tentative d'enregistrement des données ...")
            status_operation, animal = form.save_new_datas(dict_values)
            if status_operation == 1:
                mail_manager.has_to_send_mail('creation', [animal.owner], animal.id)
                print(f"> un mail a été envoyé suite à cet ajout à {animal.owner.mail}")
                return redirect("sheet:index")
            else:
                print('Echec, raison :')
                context['errors'] = status_operation
                print("j'envoie ce rapport à js : \n")
                print("***\n\t",context['errors']['alert'],"\n***\n")
                print(context['errors'])
                return render(request, 'sheet/form_anim.html', context)
        else:
            print("form not valid")
            context['errors'] = form.errors.items()
            print("\n\n*** E R R O R ***\n")
            print(form.errors.items())
            print("\n*** E N D ***\n\n")
            print(request.POST, 'et', request.FILES)
            return render(request, 'sheet/form_anim.html', context)

class AlterSheetView(View):
    """ displays the page that can modify the db """
    context = {'title': "Page Modification Fiche", 'submit_btn': "Modifier"}
    def get(self, request, given_id):
        """ display informations and form """
        owners = Owner.objects.all()
        given_values = utils_sheet.get_data_for_alter(given_id)
        print("AlterSheetView > ", given_values)
        form = SheetForm(request.POST or None, initial=given_values)
        #I need to get the concerned animal corresponding this given_id
        animal = utils_sheet.get_animal_from_given_id(given_id)[0]
        owners = Owner.objects.all()
        self.context.update({'form' : form, 'animal' : animal,  "owners" : owners, "given_values":given_values})
        return render(request, 'sheet/form_anim.html', self.context)

    def post(self, request, given_id):
        """ picks up the data in order to modify the db """
        owners = Owner.objects.all()
        given_values = utils_sheet.get_data_for_alter(given_id)
        form = SheetForm(request.POST or None, initial=given_values)
        self.context.update({'form' : form})
        dict_values = request.POST.dict()
        print(dict_values)
        pass

        if form.is_valid():
            print("alter > form is valid")
            print(f"> \t{dict_values}")
            # print("\t3/ Tentative d'enregistrement des données ...")
            success, response = utils_sheet.manage_modify_datas(given_id, dict_values)
            print('---end modify_datas')
            if success:
                print(f'{response} changement(s)')
                return redirect("sheet:index")
            else:
                self.context["error"] = response  
                return render(request, 'sheet/form_anim.html', self.context)
        self.context['error'] = form.errors.items()
        # print("\n\n*** E R R O R ***\n")
        print(form.errors.items())
        # print("\n*** E N D ***\n\n")
        print(request.POST, 'et', request.FILES)
        return render(request, 'sheet/form_anim.html', self.context)

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
        context = {"selected_owner":selected_owner,'title': "Page Modification Fiche",
         'form':form, 'animals':animals}
        return render(request, "sheet/alter_owner.html", context)

    def post(self, request, given_id, action=None):
        """this function handles post request for alter_owner page"""
        print(f"action :", action)
        form = JustOwnerForm(request.POST or None)
        selected_owner = Owner.objects.get(id=given_id)
        context = {"selected_owner":selected_owner,'form':form, 
        'title': "Page Modification Fiche",}
        dict_values = request.POST.dict()
        if action == "delete":
            print("demande suppression de Owner dont id = ", given_id)
            success, message = utils_sheet.remove_owner(given_id)
            if success:
                return redirect("sheet:index", own=1)
            else:
                return HttpResponse(message)
        elif action == "modify":
            del dict_values['csrfmiddlewaretoken']
            success, message = utils_sheet.modify_owner(given_id, dict_values)
            if success:
                print(message)
                return redirect("sheet:index", own=1)
            else:
                context['error'] = message
                # print(" * * *")
                # print(context)
                # print(" * * *")
                return render(request, "sheet/alter_owner.html", context)

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
        context = {'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        # print(dict_values)
        if form.is_valid:
            # print("form is valid")
            success, message = utils_sheet.create_owner(dict_values)
            if success:
                return redirect("sheet:index", own=1)
            context['error'] = message
            # print(" * * *")
            # print(context)
            # print(" * * *")
            return render(request, "sheet/add_owner.html", context)
        context['error'] = 'Remplissez tous les champs'
        return render(request, "sheet/add_owner.html", context)

class ContactOwnerView(View):
    """class for page historic"""
    context = {'button_value': button_value}
    def get(self, request, given_id=None, action=None):
        """this method displays historic of contact for a given owner """
        owner = Owner.objects.get(id=given_id)
        contacts = Contact.objects.filter(owner=owner)
        self.context.update({"owner": owner, "contacts": contacts, 
            'historic_cols': historic_cols})
        return render(request, "sheet/historic.html", self.context)

    def post(self, request, given_id=None, action=None):
        """this method handles a post request for the  historic of contact page """
        print(request.POST.getlist('id_check[]'))
        print("\t>Je reçois une demande de type : ", action)
        dict_values = request.POST.dict()
        print(f"t>Je  reçois {len(dict_values)} données: ", dict_values)
        owner = Owner.objects.get(id=given_id)
        contacts = Contact.objects.filter(owner=owner)
        self.context.update({"owner" : owner, "contacts": contacts})
        
        if action == "add":
            success, message = mail_manager.create_contact(owner, dict_values)
            if success:
                return JsonResponse({"data":f'{success}{message}'}, safe=False)
            # print(message)
        elif action == "remove":
            success, message = utils_sheet.remove_contact(request.POST.getlist('id_check[]'))
            # print('//////')
            # print(success, message)
            # print('//////')
            if success:
                return JsonResponse({"data":f'{success}{message}'}, safe=False)
        elif action == "modify":
            # print("alors je modifie et ...")
            success, message = utils_sheet.modify_contact(dict_values)
            print(success, message)
            if success:
                # print("je retourne : ", message)

                return JsonResponse({"data":f'{success}{message}'}, safe=False)
            # print(message)
        return render(request, "sheet/historic.html", self.context)

class AddOwnerOpenSheetView(View):
    """class for page owner_open add"""
    context = {"title" : "Nouveau Propriétaire", "submit_btn": "Ajouter"}
    def get(self, request):
        """this function handles the get request for add_owner page"""
        print(">>>OPEN add")
        form = JustOwnerForm()
        self.context['form'] = form
        return render(request, "sheet/form_owner_open.html", self.context)

    def post(self, request):
        """this function handles the post request for add_owner page"""
        print(">>>OPEN add")
        form = JustOwnerForm(request.POST)
        self.context = {'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        print(dict_values)
        if form.is_valid:
            success, message = utils_sheet.create_owner(dict_values)
            if success:
                return HttpResponse('<script type="text/javascript">window.close()</script>')
            else:
                self.context['error'] = message
                print(" * * *")
                print(self.context)
                print(" * * *")
                return render(request, "sheet/form_owner_open.html", self.context)
        self.context['error'] = 'Remplissez tous les champs'
        return render(request, "sheet/form_owner_open.html", self.context)

class AlterOwnerOpenSheetView(View):
    """class for page owner_open alter"""
    context = {"title" : "Modification Propriétaire", "submit_btn": "Modifier"}
    def get(self, request, given_id):
        """this function handles get request for alter_owner page"""
        selected_owner = Owner.objects.get(id=given_id)
        initial_dict = {
        "owner_name" :  selected_owner.owner_name,
        "owner_surname" :  selected_owner.owner_surname,
        "owner_sex": selected_owner.owner_sex,
        "mail": selected_owner.mail,
        "phone": selected_owner.phone,}
        form = JustOwnerForm(request.POST or None, initial = initial_dict)
        animals = Animal.objects.filter(owner=selected_owner)
        self.context.update({"selected_owner":selected_owner, 'form':form, 'animals':animals})
        print(self.context)
        return render(request, "sheet/form_owner_open.html", self.context)

    def post(self, request, given_id):
        """this function handles post request for alter_owner page"""
        print(">>>OPEN alter")
        form = JustOwnerForm(request.POST or None)
        self.context['form'] = form
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        print('valeurs reçues : ', dict_values)
        success, message = utils_sheet.modify_owner(given_id, dict_values)
        if success:
            # print("1", message)
            return HttpResponse('<script type="text/javascript">window.close()</script>')

        self.context['error'] = message
        print(" * * *")
        print(self.context)
        print(" * * *")
        return render(request, "sheet/form_owner_open.html", self.context)
