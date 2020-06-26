from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
class DashboardView(View):
	def get(self, request):
		"""display dashboard"""
		return HttpResponse("dashboard page")