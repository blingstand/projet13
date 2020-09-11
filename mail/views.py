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
        {'name' : 'ajouter',    'id' : 'add', 'function' : 'add()'}, 
        {'name' : 'modifier',   'id' : 'alter', 'function' : 'alter()'},
        {'name' : 'supprimer',  'id' : 'remove', 'function' : 'remove()'}],
            'mails' : mails}
        return render(request, 'mail/index.html', context)

    def post(self, request):
        """receives data to pass to deals with the dropSheet function"""
        print('*******')   
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
    def get(self, request, mail_id=None):
        """ this function displays the form"""
        form = ContentMail()
        context = {
            'form' : form}
        if mail_id: 
            mail = ut.get_mail_from_id(mail_id)
            mail.full_text = ut.modify_text(mail.full_text)[0]
            print(mail.full_text)
            context["mail"] = mail 
        return render(request, 'mail/content.html', context)

    def post(self, request):
        """ this function deals with the datas from the form"""
        form = ContentMail(request.POST)
        ut = Utils()
        dict_values = {'overview':'0', 'mail_id':None}
        print("- - - - - ")
        print(dict_values, type(dict_values))
        print(dict_values.keys())
        print(dict_values['overview'] == '0')
        dict_values.update(request.POST.dict())
        print("- - - - - ")
        print(dict_values, type(dict_values))
        print(dict_values.keys())
        print(dict_values['overview'] == '0')
        print("- - - - - ")
        #Django form ...
        if dict_values['mail_id'] != None:
            mail_id = dict_values['mail_id']
            #with mail_id -> mail exists -> alter db 
            print('alter db then redirect')
            print(dict_values['overview'] == '0')
            mail = ut.alter_db(dict_values)
        else:
            #no mail_id -> create a new mail
            print('save then redirect')
            mail_id = ut.save_datas(dict_values)
            mail = ut.get_mail_from_id(mail_id)
        print(dict_values['overview'] == '0')
        if dict_values['overview'] == '0':
            context = {'mail' : mail}
            return render(request, 'mail/cns.html', context)
        elif dict_values['overview'] == '1': 
            #AJAX request before overview
            print("juste un aperçu")
            return JsonResponse({"mail_id" : mail_id}, safe=False)
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
            print(mail.send_at_this_date)
            context["mail"] = mail 
        return render(request, 'mail/settings.html', context)

    def post(self, request, mail_id=None):
        form = SettingsMail(request.POST)
        dict_values = {'ajax':'0'}
        dict_values.update(request.POST.dict())

        if dict_values['ajax'] == "1": 
            mail = ut.get_mail_from_id(dict_values['mail_id'])
            print(mail)
            ut.change_auto_send(mail, (dict_values['auto_send']))
            return JsonResponse({"chgt" : "saved"}, safe=False)
        if form.is_valid():
            mail = ut.get_mail_from_id(mail_id)
            ut.change_auto_send(mail, True)
            ut.auto_send_false(mail)
            age, date= form.cleaned_data["age"], form.cleaned_data["date"]
            if form.cleaned_data["frequency"] == "1": 
                mail.send_after_creation = True
                print("1 > Un mail sera envoyé à la création de la fiche.")
            elif form.cleaned_data["frequency"] == "2": 
                mail.send_after_modif = True
                print("2 > Un mail sera envoyé à chaque modification de la fiche.")
            elif form.cleaned_data["frequency"] == "3": 
                mail.send_when_x_month = age
                print(f"3 > un mail sera envoyé quand l'animal aura {mail.send_when_x_month} mois")
            elif form.cleaned_data["frequency"] == "4": 
                mail.send_at_this_date = date
                print(f"4 > un mail auto sera envoyé à cette date : {mail.send_at_this_date} ")
            
            mail.save()
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


