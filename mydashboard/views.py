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
        gradat = GraphDatas()
        if request.user.is_authenticated:
            dict_value = gradat.get_list_datas
            owners, to_contact, contacted = gradat.get_list_for_search
            context={
                'nb_owners': len(owners),
                'nb_contacted':len(contacted),
                'nb_to_contact':len(to_contact)}
            return render(request, "dashboard/index.html", context)
        return redirect('user:connection')
    def error_404(request, exception):
        context = {}
        return render(request,'dashboard/error_404.html', context)

    def error_500(request):
        context = {}
        return render(request,'dashboard/error_500.html', context)
