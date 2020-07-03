from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class SheetView(View):
	def get(self, request):
		context={'button_value':['trier par', 'ajouter', 'modifier', 'supprimer']}
		return render(request, 'sheet/index.html', context)