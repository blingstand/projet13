from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
class DashboardView(View):
	def get(self, request):
		"""display dashboard"""
		# if request.user.is_authenticated:
		return render(request, "dashboard/index.html")
		# return redirect('user:connection')