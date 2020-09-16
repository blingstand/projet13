from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
class MyDashboardView(View):
    def get(self, request):
        """display dashboard"""
        if request.user.is_authenticated:
            dict_values = {'ask_graph_datas':'0'}
            dict_values.update(request.GET.dict())
            if dict_values['ask_graph_datas'] == "1": 
                datas ={
                'cont' : [1, 7, 12, 19, 23],
                'toCont' : [38, 28, 21, 20, 20],
                }
                print(datas)
                return JsonResponse(datas, safe=False)  
            context={'name': request.user.username}
            return render(request, "dashboard/index.html", context)
        return redirect('user:connection')
