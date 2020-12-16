from mydashboard.utils import GraphDatas
from mail.mail_manager import MailManager

from .utils import UtilsSheet
from .form import SheetForm, JustOwnerForm
from .models import Animal, Owner, Contact

gradat = GraphDatas()
utils_sheet = UtilsSheet()

class BuilderGet(): 
    """this class contains methods that builds context for get method"""        

    def for_sheet_view(self, own=0, action=None, search=0): 
        """returns context"""
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
            owners = list(owners)

        elif action == "search:prop":
            owners = Owner.objects.get(id=search),
        
        elif action == "search:anim":
            animals = Animal.objects.get(id=search),

        
        context = {
            'animals' : animals, 'owners': owners, 'disp_owners': own
            }
        return context

    def for_add_sheet_view(self, request):
        """returns context"""
        owners = Owner.objects.all()
        form = SheetForm(request.POST or None)
        context = {'form' : form, "owners" : owners}
        return context

    def for_add_owner_open_sheet_view(self): 
        """returns context"""
        form = JustOwnerForm()
        context = {'form': form}
        return context

    def for_alter_sheet_view(self, given_id, request):
        """ returns context """
        given_values = utils_sheet.get_data_for_alter(given_id)
        form = SheetForm(request.POST or None, initial=given_values)
        animal = utils_sheet.get_animal_from_given_id(given_id)[0]
        owners = Owner.objects.all()
        context = {'form' : form, 'animal' : animal,  "owners" : owners, "given_values":given_values}
        return context

    def for_alter_owner_open_sheet_view(self, request, given_id):
        selected_owner = Owner.objects.get(id=given_id)
        initial_dict = {
        "owner_name" :  selected_owner.owner_name,
        "owner_surname" :  selected_owner.owner_surname,
        "owner_sex": selected_owner.owner_sex,
        "mail": selected_owner.mail,
        "phone": selected_owner.phone,}
        form = JustOwnerForm(request.POST or None, initial = initial_dict)
        animals = Animal.objects.filter(owner=selected_owner)
        context = {"selected_owner":selected_owner, 'form':form, 'animals':animals}
        return context

    def for_contact_sheet_view(self, given_id): 
        owner = Owner.objects.get(id=given_id)
        contacts = Contact.objects.filter(owner=owner)
        context = {"owner": owner, "contacts": contacts}
        return context