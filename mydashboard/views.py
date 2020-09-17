from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

#this app 
from .utils import GraphDatas
# Create your views here.
gradat = GraphDatas()
class MyDashboardView(View):
    def get(self, request):
        """display dashboard"""
        if request.user.is_authenticated: 
            datas ={
            'nb_owner_with_obligations' : gradat.nb_owner_with_obligations,
            'cont' : gradat.contacted,
            'toCont' : gradat.to_contact,
            }
            print(gradat.nb_owner_with_obligations)
            context={'name': request.user.username, 'datas' : datas}
            return render(request, "dashboard/index.html", context)
        return redirect('user:connection')
