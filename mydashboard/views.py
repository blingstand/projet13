from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
class MyDashboardView(View):
	def get(self, request):
		"""display dashboard"""
		if request.user.is_authenticated:
			context={'name': request.user.username}
			return render(request, "dashboard/index.html", context)
		return redirect('user:connection')