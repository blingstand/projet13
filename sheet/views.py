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
from .form import SheetForm, JustOwnerForm
from .models import Animal, Owner, Contact
from .utils import UtilsSheet
from .datas import *
from .build_get import BuilderGet
from .build_post import BuilderPost

# Create your views here.

gradat = GraphDatas()
mail_manager = MailManager()
utils_sheet = UtilsSheet()
g_builder = BuilderGet()
p_builder = BuilderPost()

def redirect_index(request):
    return redirect('sheet:index')
class SheetView(View):
    """class for page index sheet"""
    context = {'top_columns_anim': top_columns_anim, 'top_columns_owner': top_columns_owner, 
            'button_value': button_value}
    def get(self, request, own=0, action=None, search=0):
        """3 actions :
            1/ displays anim sheet list from db 
            2/ displays owner sheet list from db 
            3/ displays result of search 
        """
        print( f"\n------- {self.__class__.__name__}/get -------")
        print(f"own={own}, action={action}, search={search}")

        add_context = g_builder.for_sheet_view(own, action, search)
        self.context.update(add_context)
        print( f"le server envoie :\n{self.context.keys()}\n")
        return render(request, 'sheet/index.html', self.context)

    def post(self, request, own, search=0):
        """receives data and triggers dropSheet(data)"""
        print( f"\n------- {self.__class__.__name__}/post -------")
        given_id = request.POST.getlist('checkbox')
        print(f"own={own}, given_id={given_id}")
        p_builder.for_sheet_view(own,given_id)
        return redirect("sheet:index",own=own)

class AddSheetView(View):
    """class for page add sheet"""
    context = {'title': "Page Ajout Fiche", 'submit_btn': "Ajouter"}
    def get(self, request):
        #displays the page
        print( f"\n------- {self.__class__.__name__}/get -------")
        print(f"pas de paramètres")

        add_context = g_builder.for_add_sheet_view(request)
        self.context.update(add_context)
        print( f"le server envoie :\n{self.context.keys()}\n")
        return render(request, 'sheet/form_anim.html', self.context)

    def post(self, request):
        #handles the form and the errors
        print( f"\n------- {self.__class__.__name__}/post -------")
        condition, response = p_builder.for_add_sheet_view(request)
        self.context.update(response)

        if condition == "ajax": 
            return JsonResponse({"data":response}, safe=False)
        elif condition == 'form_ok': 
            return redirect("sheet:index")
        else: 
            return render(request, 'sheet/form_anim.html', self.context)

class AlterSheetView(View):
    """ displays the page that can modify the db """
    context = {'title': "Page Modification Fiche", 'submit_btn': "Modifier"}
    def get(self, request, given_id):
        """ display informations and form """
        print( f"\n------- {self.__class__.__name__}/get -------")
        print(f"given_id : {given_id}")
        add_context = g_builder.for_alter_sheet_view(given_id, request)
        self.context.update(add_context)
        print( f"le server envoie :\n{self.context.keys()}\n")
        return render(request, 'sheet/form_anim.html', self.context)

    def post(self, request, given_id):
        """ picks up the data in order to modify the db """
        print( f"\n------- {self.__class__.__name__}/post -------")
        print(f"given_id : {given_id}")
        condition, response = p_builder.for_alter_sheet_view(request, given_id)
        self.context.update(response)
        print( f"le server envoie :\n{self.context.keys()}\n")
        
        if condition == "form_ok_success":
            return redirect("sheet:index")
        elif condition == "form_ok_error":
            return render(request, 'sheet/form_anim.html', self.context)
        elif condition == "form_not_valid":
            return render(request, 'sheet/form_anim.html', self.context)

class AddOwnerOpenSheetView(View):
    """class for page owner_open add"""
    context = {"title" : "Nouveau Propriétaire", "submit_btn": "Ajouter"}
    def get(self, request):
        """this function handles the get request for add_owner page"""
        print( f"\n------- {self.__class__.__name__}/get -------")
        print("pas de paramètres")

        add_context = g_builder.for_add_owner_open_sheet_view()
        self.context.update(add_context)
        print( f"le server envoie :\n{self.context.keys()}\n")
        
        return render(request, "sheet/form_owner_open.html", self.context)

    def post(self, request):
        """this function handles the post request for add_owner page"""
        print( f"\n------- {self.__class__.__name__}/post -------")
        print("pas de paramètres")

        condition, response = p_builder.for_add_owner_open_sheet_view(request) 
        self.context.update(response)

        if condition == "form_ok_success":
            return HttpResponse('<script type="text/javascript">window.close()</script>')
        
        return render(request, "sheet/form_owner_open.html", self.context)

class AlterOwnerOpenSheetView(View):
    """class for page owner_open alter"""
    context = {"title" : "Modification Propriétaire", "submit_btn": "Modifier"}
    def get(self, request, given_id):
        """this function handles get request for alter_owner page"""
        print( f"\n------- {self.__class__.__name__}/get -------")
        print("given_id: {given_id}")
        add_context = g_builder.for_alter_owner_open_sheet_view(request, given_id)
        self.context.update(add_context)
        print( f"le server envoie :\n{self.context.keys()}\n")
        return render(request, "sheet/form_owner_open.html", self.context)

    def post(self, request, given_id):
        """this function handles post request for alter_owner page"""
        print( f"\n------- {self.__class__.__name__}/get -------")
        print("given_id: {given_id}")
        condition, response = p_builder.for_alter_owner_open_sheet_view(request, given_id) 
        self.context.update(response)
        if condition == "form_ok":
            return HttpResponse('<script type="text/javascript">window.close()</script>')
        return render(request, "sheet/form_owner_open.html", self.context)

class ContactOwnerView(View):
    """class for page historic"""
    context = {'button_value': button_value, 'historic_cols': historic_cols}
    def get(self, request, given_id=None, action=None):
        """this method displays historic of contact for a given owner """
        print( f"\n------- {self.__class__.__name__}/get -------")
        print("given_id: {given_id}")
        add_context = g_builder.for_contact_sheet_view(given_id)
        self.context.update(add_context)
        print( f"le server envoie :\n{self.context.keys()}\n")

        return render(request, "sheet/historic.html", self.context)

    def post(self, request, given_id=None, action=None):
        """this method handles a post request for the  historic of contact page """
        
        print( f"\n------- {self.__class__.__name__}/get -------")
        print(f"given_id: {given_id}, action: {action}")
        condition, response = p_builder.for_contact_sheet_view(request, given_id, action) 
        self.context.update(response)
        
        if condition != "error":
            return JsonResponse(response, safe=False)
        return render(request, "sheet/historic.html", self.context)
