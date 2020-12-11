from mydashboard.utils import GraphDatas
from mail.mail_manager import MailManager

from .form import SheetForm, JustOwnerForm
from .models import Animal, Owner, Contact
gradat = GraphDatas()

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
            animals = Animal.objects.get(id=search)
        
        context = {
            'animals' : animals, 'owners': owners, 'disp_owners': own}
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