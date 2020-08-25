from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Mail
from .form import SettingsMail, ContentMail
# Create your views here.
class MailView(View):
    def get(self, request):
        mails = Mail.objects.all()
        mails = [mail for mail in mails]
        context={
            'button_value': ['imprimer', 'ajouter', 'supprimer', 'modifier'], 
            'mails' : mails}
        return render(request, 'mail/index.html', context)

class CNSView(View):
    """this class organize the choices """
    def get(self, request):
        return render(request, 'mail/cns.html')

class ContentView(View):
    """ this class handles the content of an automatic mail"""
    def get(self, request):
        """ this function displays the form"""
        form = ContentMail()
        context = {
            'form' : form}
        return render(request, 'mail/content.html', context)

    def post(self, request):
        """ this function deals with the datas from the form"""
        form = ContentMail(request.POST)
        if form.is_valid():
            pass
        context = {
            'form' : form}
        return render(request, 'mail/content.html', context)


class SettingsView(View):
    def get(self, request):
        form = SettingsMail()
        context = {
            'form' : form}
        return render(request, 'mail/settings.html', context)

    def post(self, request):
        form = SettingsMail(request.POST)
        if form.is_valid():
            age, date= form.cleaned_data["age"], form.cleaned_data["date"]
            print("***********")
            print(f"\nreçu : {request.POST}")
            print(form.cleaned_data["frequency"])
            print("***********")
            if form.cleaned_data["frequency"] == "1": 
                print("1")
            elif form.cleaned_data["frequency"] == "2": 
                print("2")
            elif form.cleaned_data["frequency"] == "3": 
                print(f"3 > {age} ")
                pass
            elif form.cleaned_data["frequency"] == "4": 
                print(f"4 > {date} ")
                pass

        return HttpResponse('bravo')
        print("error")
        print(form.errors.items())
        print(f"\ndebug : {request.POST}")
        context = {
            'form' : form}
        return render(request, 'mail/settings.html', context)

