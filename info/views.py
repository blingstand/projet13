from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


class InfosView(View):
	def get(self, request):
		return render(request, 'info/index.html')

class LegalNoticeView(View):
	def get (self, request):
		return render(request, 'info/legal_notice.html')