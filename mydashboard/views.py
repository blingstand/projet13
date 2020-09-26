from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View



#this app 
# from .utils import GraphDatas
# from .models import GraModel
# # Create your views here.
# gradat = GraphDatas()
# gramod = GraModel()
class MyDashboardView(View):
    def get(self, request):
        """display dashboard"""
        # date = datetime.now().date()
        # print(date.strftime("%d/%m/%y"))
        # record_day = 21 in(1,7,14,21,28)
        # if record_day and len(GraModel.objects.filter(date=date)) == 0:
        #     gram = GraModel(
        #         date = date,
        #         nb_owners=gradat.nb_owner_with_obligations,
        #         nb_contacted=gradat.contacted,
        #         nb_to_contact=gradat.to_contact)
        #     print(gram)

        if request.user.is_authenticated:
            # prevData = gradat.getPrevData() 
            # datas ={
            # 'nb_owner_with_obligations' : gradat.nb_owner_with_obligations,
            # 'cont' : prevData['contacted']+[gradat.contacted],
            # 'toCont' : prevData['to_contact']+[gradat.to_contact],
            # 'date' : prevData['date']+[date.strftime("%d/%m/%y")],
            # 'current_cont': gradat.contacted, 
            # 'current_to_cont': gradat.to_contact, 
            # }
            # context={'name': request.user.username, 'datas' : datas}
            return render(request, "dashboard/index.html", context)
        return redirect('user:connection')
