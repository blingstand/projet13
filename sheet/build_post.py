from mydashboard.utils import GraphDatas

from mail.mail_manager import MailManager
from mail.models import Mail
from .utils import UtilsSheet
from .form import SheetForm, JustOwnerForm
from .models import Animal, Owner, Contact
gradat = GraphDatas()
mail_manager = MailManager()
utils_sheet = UtilsSheet()

class BuilderPost(): 
    """this class contains methods that builds context for get method"""        
    def for_sheet_view(self, own, given_id): 
        """build post response"""
        if own == 0:
            for_mail = utils_sheet.drop_sheet(given_id) #bloqué suppression
        else:
            utils_sheet.remove_owner(given_id)

        if for_mail[0]:
            owner_to_contact, given_id = for_mail[1:3]
            mail_manager.has_to_send_mail(Mail.DA, owner_to_contact, given_id) #DA = Delete Animal 
            print(f">> mail envoyé à {owner_to_contact}")

    def for_add_sheet_view(self, request): 
        """build post response
            1/ ajax request -> ajax response
            2/ form ok -> send mail -> return index
            3/ form error -> return form + display error
        """
        #var
        owners = Owner.objects.all()
        form = SheetForm(request.POST or None)
        ajax_search_owner_data = {"value": ""}
        dict_values = request.POST.dict()
        ajax_search_owner_data.update(dict_values)
        context = {'form' : form, "owners" : owners}
        print(f"clé reçues : ", dict_values.keys())
        #conditions
        if ajax_search_owner_data['value'] != "":
            response = utils_sheet.search_owner(ajax_search_owner_data)
            return 'ajax', response
    
        if form.is_valid(): #new entry + mail 
            dict_values = form.from_form()
            status_operation, animal = form.save_new_datas(dict_values)
            
            if status_operation == 1:
                # 2 types of mails > for anim neutered and anim not neutered
                #make a diff
                condition = Mail.CAS if animal.admin_data.is_neutered == 1 else Mail.CANS
                mail_manager.has_to_send_mail(condition, [animal.owner], animal.id)
                print(f">> mail envoyé à {[animal.owner]}")
                return "form_ok", context
            
            else:
                print('Echec, raison :')
                context['errors'] = status_operation
                print("j'envoie ce rapport à js : \n")
                print("***\n\t",context['errors']['alert'],"\n***\n")
                print(context['errors'])
                return "form_error", context
        
        else:
            print("form not valid")
            context['errors'] = form.errors.items()
            print("\n\n*** E R R O R ***\n")
            print(form.errors.items())
            print("\n*** E N D ***\n\n")
            print(request.POST, 'et', request.FILES)
            return "form_error", context

    def for_alter_sheet_view(self, request, given_id): 

        owners = Owner.objects.all()
        given_values = utils_sheet.get_data_for_alter(given_id)
        form = SheetForm(request.POST or None, initial=given_values)
        context = {'form': form}
        dict_values = request.POST.dict()

        if form.is_valid():
            success, response, mail_to_send = utils_sheet.manage_modify_datas(given_id, dict_values)
            if success:
                conditions, owner_to_contact, given_id = mail_to_send
                for condition in conditions: 
                    mail_manager.has_to_send_mail(condition, owner_to_contact, given_id)
                return 'form_ok_success', context
            else:
                context["error"] = response  
                return 'form_ok_error', context
        #form not valid
        context['error'] = form.errors.items()
        return 'form_not_valid', context

    def for_add_owner_open_sheet_view(self, request): 
        form = JustOwnerForm(request.POST)
        context = {'form':form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        if form.is_valid:
            success, message = utils_sheet.create_owner(dict_values)
            if success:
                 return 'form_ok_success', context
            else:
                context["error"] = response  
                return 'form_error', context
        #form not valid
        context['error'] = form.errors.items()
        return 'form_not_valid', context

    def for_alter_owner_open_sheet_view(self, request, given_id):
        form = JustOwnerForm(request.POST or None)
        context = {'form': form}
        dict_values = request.POST.dict()
        del dict_values['csrfmiddlewaretoken']
        success, message = utils_sheet.modify_owner(given_id, dict_values)
        if success:
            return "form_ok", context
        else:
            context['error'] = message
            print(" * * *")
            print(context)
            print(" * * *")
            return "form_invalid", context

    def for_contact_sheet_view(self, request, given_id, action):
        dict_values = request.POST.dict()
        owner = Owner.objects.get(id=given_id)
        contacts = Contact.objects.filter(owner=owner)
        context = {"owner" : owner, "contacts": contacts}
        success = False
        if action == "add":
            success, message = mail_manager.create_contact(owner, dict_values)
        elif action == "remove":
            success, message = utils_sheet.remove_contact(request.POST.getlist('id_check[]'))
        elif action == "modify":
            success, message = utils_sheet.modify_contact(dict_values)
        if success:
            return "success", {"data":f'{success}{message}'}
        context["error"] = message
        return "error", context