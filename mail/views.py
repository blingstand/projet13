from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Mail
from .form import SettingsMail, ContentMail
from .utils import Utils

from sheet.models import Animal

ut = Utils()
# Create your views here.
class MailView(View):
    def get(self, request):
        mails = Mail.objects.all()
        mails = [mail for mail in mails]
        context={
            'button_value':[
        {'name' : 'imprimer',  'id' :'print', 'function' : 'print()'},
        {'name' : 'ajouter',    'id' : 'add', 'function' : 'Add()'}, 
        {'name' : 'modifier',   'id' : 'alter', 'function' : 'Alter()'},
        {'name' : 'supprimer',  'id' : 'remove', 'function' : 'Remove()'}],
            'mails' : mails}
        return render(request, 'mail/index.html', context)

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
    def get(self, request,mail_id=None):
        context = {}
        if mail_id is not None: 
            mail = ut.get_mail_from_id(mail_id)
            context['mail'] = mail
        return render(request, 'mail/cns.html', context)

class ContentView(View):
    """ this class handles the content of an automatic mail"""
    def get(self, request, mail_id=0):
        """ this function displays the form"""
        form = ContentMail()
        context = {
            'form' : form}
        print('get', mail_id)
        if mail_id != 0: 
            mail = ut.get_mail_from_id(mail_id)
            print("avant ut.modify_text")
            print(mail.full_text)
            mail.full_text = ut.modify_text(mail.full_text)[0]
            context["mail"] = mail 
        return render(request, 'mail/content.html', context)

    def post(self, request, mail_id=0, action=None):
        """ this function deals with the datas from the form"""
        form = ContentMail(request.POST)
        ut = Utils()
        dict_values = request.POST.dict()
        print("- - - - - ")
        print(dict_values)
        print(mail_id, action)
        print("- - - - - ")
        # if dict_values['checkIntegrity'] == '1': 

        #Django form ...
        if mail_id != 0:
            #with mail_id -> mail exists -> alter db 
            print('alter db')
            mail = ut.alter_db(dict_values, mail_id)
        else:
            #no mail_id -> create a new mail
            print('save')
            mail_id = ut.save_datas(dict_values)
            mail = ut.get_mail_from_id(mail_id)
        if action == None:
            context = {'mail' : mail}
            return render(request, 'mail/cns.html', context)
        elif action == 'overview': 
            #AJAX request before overview
            print("juste un aperçu")
            return JsonResponse({"data" : mail_id}, safe=False)
        elif action == 'check_integrity':
            #check if title is unique
            queryset = Mail.objects.filter(title=dict_values['title'])
            if len(queryset) >= 1:
                return JsonResponse({"data" : "1"}, safe=False) 
            return JsonResponse({"data" : "0"}, safe=False) 

        else:
            return HttpResponse(('Il y a une erreur :/'))

class OverviewView(View):
    """ this class handles the views for overview.html """
    def get(self, request, mail_id):
        form = ContentMail()
        ut = Utils()
        animal = Animal.objects.all()[0]
        print(request.GET)
        mail = ut.get_mail_from_id(mail_id)
        mail.full_text = ut.modify_text(mail.full_text)[1]
        context = {
            'form' : form, 'mail' : mail, 'animal' : animal}
        return render(request, 'mail/overview.html', context)

class SettingsView(View):
    def get(self, request, mail_id=None):
        form = SettingsMail()
        context = {
            'form' : form}
        if mail_id: 
            mail = ut.get_mail_from_id(mail_id)
            context["mail"] = mail 
        return render(request, 'mail/settings.html', context)

    def post(self, request, mail_id=None):
        form = SettingsMail(request.POST)
        dict_values = {'ajax':'0'}
        dict_values.update(request.POST.dict())

        if dict_values['ajax'] == "1": 
            mail = ut.get_mail_from_id(dict_values['mail_id'])
            ut.change_auto_send(mail, (dict_values['auto_send']))
            if dict_values['auto_send'] == "1":
                mail.send_after_creation = True
                mail.save()
            return JsonResponse({"chgt" : "saved"}, safe=False)
        if form.is_valid():
            mail = ut.get_mail_from_id(mail_id)
            ut.change_auto_send(mail, True)
            ut.auto_send_false(mail)

            age, date= form.cleaned_data["age"], form.cleaned_data["date"]
            if form.cleaned_data["frequency"] == "1": 
                mail.send_after_creation = True
                # print("1 > Un mail sera envoyé à la création de la fiche.")
            elif form.cleaned_data["frequency"] == "2": 
                mail.send_after_modif = True
                # print("2 > Un mail sera envoyé à chaque modification de la fiche.")
            elif form.cleaned_data["frequency"] == "3": 
                mail.send_when_x_month = age
                # print(f"3 > un mail sera envoyé quand l'animal aura {mail.send_when_x_month} mois")
            elif form.cleaned_data["frequency"] == "4": 
                mail.send_at_this_date = date
                # print(f"4 > un mail auto sera envoyé à cette date : {mail.send_at_this_date} ")
            
            mail.save()
            print(mail.auto_send)
            context = {'mail' : mail}
            return render(request, 'mail/cns.html', context)
        context = {'form' : form}
        return render(request, 'mail/settings.html', context)
        print("error")
        print(form.errors.items())
        print(f"\ndebug : {request.POST}")
        context = {
            'form' : form}
        return render(request, 'mail/settings.html', context)


