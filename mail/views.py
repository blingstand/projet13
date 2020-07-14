from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Mail
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
	def get(self, request):
		return render(request, 'mail/cns.html')

class ContentView(View):
	def get(self, request):
		return render(request, 'mail/content.html')

class SettingsView(View):
	def get(self, request):
		return render(request, 'mail/settings.html')