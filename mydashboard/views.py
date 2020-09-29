from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

 

#this app 
from .utils import GraphDatas
from .models import GraModel
# Create your views here.
gradat = GraphDatas()
gramod = GraModel()
class MyDashboardView(View):
    def get(self, request):
        """display dashboard"""
        if request.user.is_authenticated:
            dict_value = gradat.get_list_datas
            owners, to_contact, contacted = gradat.get_list_for_search
            context={
                'nb_owners': len(owners),
                'nb_contacted':len(contacted),
                'nb_to_contact':len(to_contact)}
            return render(request, "dashboard/index.html", context)
        return redirect('user:connection')
