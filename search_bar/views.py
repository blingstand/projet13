from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

# Create your views here.
class SearchBarView(View): 
	def post(self, request): 
		return HttpResponse('recherche en cours')