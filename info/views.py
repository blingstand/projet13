from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class InfosView(View):
	def get(self, request):
		return HttpResponse('page info')