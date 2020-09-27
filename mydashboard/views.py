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
            print(gradat)
            print(gradat.anim_with_caution)
            print("> ", gradat.get_list_datas)
            print("contacted : ", gradat.contacted_or_to_contact[0])
            print("to contact : ", gradat.contacted_or_to_contact[1])
            datas = "ok"
            context={'name': request.user.username, 'datas' : datas}
            return render(request, "dashboard/index.html", context)
        return redirect('user:connection')
