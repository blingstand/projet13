from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
class LegalNoticeView(View):
	def get(self, request):
		return HttpResponse("page de legal notice")
