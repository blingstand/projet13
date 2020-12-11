from mydashboard.utils import GraphDatas
from mail.mail_manager import MailManager

from .utils import UtilsSheet
from .form import SheetForm, JustOwnerForm
from .models import Animal, Owner, Contact
gradat = GraphDatas()

utils_sheet = UtilsSheet()

class BuilderPost(): 
    """this class contains methods that builds context for get method"""        
    def for_sheet_view(self, own, given_id): 
        """build post response"""
        if own == 0:
            utils_sheet.drop_sheet(given_id)
        utils_sheet.remove_owner(given_id)
        return 1

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
                print(f"> un mail a été envoyé suite à cet ajout à {animal.owner.mail}")
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