"""views for the mail app """
#from django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
# from other app
from sheet.models import Animal
#from this app
from .models import Mail
from .form import SettingsMail, ContentMail
from .utils import UtilsMail
from .data import options_animal, options_owner, options_admin
ut = UtilsMail()
# Create your views here.
class MailView(View):
    """ this class manages index page """
    def get(self, request):
        """ returns the mail index page"""
        mails = Mail.objects.all()
        mails = [mail for mail in mails]
        context={
            'button_value':[
        {'name' : 'ajouter',    'id' : 'add', 'function' : 'Add()'},
        {'name' : 'modifier',   'id' : 'alter', 'function' : 'Alter()'},
        {'name' : 'supprimer',  'id' : 'remove', 'function' : 'Remove()'}],
            'mails' : mails}
        print(mails[0].get_condition)
        return render(request, 'mail/index.html', context)
        #test
    def post(self, request):
        """receives data to pass to deals with the dropSheet function"""
        print('*******')
        print(type(request.POST))
        print(request.POST)
        print('*******')
        given_id = request.POST.getlist('checkbox')
        print('Avant supression :') #affichage de vérification
        print(f'\t{len(Mail.objects.all())} mails dans la base.')
        ut.drop_mail(given_id)
        print('Après supression :')
        print(f'\t{len(Mail.objects.all())} mails dans la base.')
        return redirect("mail:index")
class CNSView(View):
    """this class organize the choices """
    def get(self, request, mail_id=None):
        context = {}
        if mail_id is not None:
            mail = ut.get_mail_from_id(mail_id)
            context['mail'] = mail
        return render(request, 'mail/cns.html', context)
class ContentView(View):
    """ this class handles the content of an automatic mail"""
    context = {"options_animal": options_animal, "options_owner": options_owner, "options_admin": options_admin, }
    def get(self, request, mail_id=0):
        """ this function displays the form"""
        print("- - - - - get ")
        form = ContentMail()
        
        if mail_id != 0:
            mail = ut.get_mail_from_id(mail_id)
            values = {
            "title" : mail.title,
            "resume" : mail.resume,
            "plain_text" : mail.plain_text,
            }
            form = ContentMail(initial = values)
            self.context["mail"] = mail
            print(dir(form))
            print(form.initial)
        self.context['form'] = form
        return render(request, 'mail/content.html', self.context)
   
    def post(self, request, mail_id=0, action=None):
        """ this function deals with the datas from the form"""
        dict_values = request.POST.dict()
        print("- - - - - post ")
        print(f'mail_id : {mail_id}, action : {action}')
        print("values :\n", dict_values)
        print("- - - - - ")
        # if dict_values['checkIntegrity'] == '1':
        if action == 'check_integrity':
            #check if title is unique
            queryset = Mail.objects.filter(title=dict_values['title'])
            if len(queryset) >= 1:
                return JsonResponse({"data" : "1"}, safe=False)
            return JsonResponse({"data" : "0"}, safe=False)
        #Django form ...
        if mail_id != 0:
            print('alter pour id = ', mail_id)
            #with mail_id -> mail exists -> alter db
            mail = ut.alter_db(dict_values, mail_id)
            print(mail)
        else:
            #no mail_id -> create a new mail
            print('save')
            mail_id = ut.save_datas(dict_values)
            mail = ut.get_mail_from_id(mail_id)
        if action == None:
            return redirect('mail:cns', mail_id=mail.mail_id)
        elif action == 'overview':
            #AJAX request before overview
            print("juste un aperçu")
            return JsonResponse({"data" : mail_id}, safe=False)
        else:
            return HttpResponse(('Il y a une erreur :/'))
class OverviewView(View):
    """ this class handles the views for overview.html """
    def get(self, request, mail_id):
        """ returns overview with an self filled form"""
        mail = ut.get_mail_from_id(mail_id)
        values = {
            "title" : mail.title,
            "resume" : mail.resume,
            "plain_text" : mail.modified_text,
        }
        form = ContentMail(initial = values)
        animal = Animal.objects.all()[0]
        context = {
            'form' : form, 'mail' : mail, 'animal' : animal}
        return render(request, 'mail/overview.html', context)
class SettingsView(View):
    """ class for settings page"""
    def get(self, request, mail_id):
        """ response different if gets mail id"""
        print("--- get SettingsView -----" )
        mail = ut.get_mail_from_id(mail_id)
        form = SettingsMail(initial={'condition' : mail.condition})
        print(form.fields)
        context = {"mail": mail, "form": form}
        print("\t" , mail, "auto_send", mail.auto_send_js)
        print("\t" , mail.condition, "*****")
        return render(request, 'mail/settings.html', context)
    def post(self, request, mail_id):
        """ can manage ajax req and form """
        print("--- post SettingsView -----" )
        mail = ut.get_mail_from_id(mail_id)
        form = SettingsMail(request.POST, )
        dict_values = {'ajax':'0'}
        dict_values.update(request.POST.dict())
        print("\tajax : " ,dict_values['ajax'])
       
        if dict_values['ajax'] == "1": #change auto send 
            ut.change_auto_send(mail, (dict_values['auto_send']))
            print('\tauto_send : ', mail.auto_send)
            return JsonResponse({"auto_send" : dict_values['auto_send']}, safe=False)
        
        if form.is_valid():                     #means 1 condition is selected
            mail.send_after_creation = True     #auto_send activated
            mail.condition = form.cleaned_data["condition"]
            mail.save()
            context = {'mail' : mail}
            return render(request, 'mail/cns.html', context)
      
        context = {
            'form' : form}
        return render(request, 'mail/settings.html', context)
