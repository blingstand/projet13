from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from .utils import Utils
utils = Utils()

# Create your views here.
class SearchBarView(View): 
	def post(self, request): 
		dict_value = request.POST.dict()
		input_value = dict_value['value']
		list_response = utils.answering(input_value)
		print("****")
		print("post123 :", list_response)
		print("****")
		return JsonResponse({'data':list_response}, safe=False) 