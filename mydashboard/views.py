from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

 

#this app 
from .utils import GraphDatas

# Create your views here.
class MyDashboardView(View):
    def get(self, request):
        """display dashboard"""
        print("--- get ---\n")
        gradat = GraphDatas()
        date, list_to_contact, list_contacted = gradat.get_list_datas
        if request.user.is_authenticated:
            try:
                owners, to_contact, contacted = gradat.get_list_for_search
                print("*****")
                print(f"returned : \n{owners}, \n{to_contact}, \n{contacted}")
                context={ 
                    "date" : date,
                    'nb_owners': len(owners),
                    'nb_contacted':len(contacted),
                    'nb_to_contact':len(to_contact), 
                    'list_to_contact':list_to_contact, 
                    'list_contacted' : list_contacted,
                    }
                print(context)
                print("\n--- end ---")
                return render(request, "dashboard/index.html", context)
            except:
                pass
        return redirect('user:connection')
    def error_404(request, exception):
        context = {}
        return render(request,'dashboard/error_404.html', context)

    def error_500(request):
        context = {}
        return render(request,'dashboard/error_500.html', context)
