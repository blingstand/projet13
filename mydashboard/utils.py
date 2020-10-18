#from python
from datetime import datetime, timedelta

#from django
from django.db import models

# from current app
from .models import GraModel

#from other apps
from sheet.models import *
 
# Create your models here.
class GraphDatas():
    """ All the datas that graph needs to be built """
    def __init__(self):
        self.anim_with_caution = Animal.objects.filter(caution__gt=0)
        self.now = datetime.now().date()
        self.year, self.month = self.now.year , self.now.month
        self.day = self.now.day
        self.list_imp_date = [1, 7, 14, 21, 28]
        self.two_weeks = timedelta(days = 14)
        self.owners = self.get_owners_with_obligations()

        print("self.owners = ", self.owners)

    def get_owners_with_obligations(self):
        """ returns list owners with caution"""
        owners = [owner if owner.sum_caution > 0 else 'vide' for owner in Owner.objects.all()]
        owners = list(filter(lambda exp: exp != "vide", owners))
        return owners
    @property
    def get_list_datas(self):
        """ this functions returns a list of dict. 
        Each dict contains owner, date_of_adoption, last_contact
        """
        print("nous sommes le : ", self.day)
        print("relevé pour le mois de : ", self.now.strftime("%B"))
        
        list_to_contact_final, list_contacted_final = [], []
        print(len(self.owners), "propriétaires avec obligations")
        for imp_dat in self.list_imp_date: 
            print("--\nA la date du :  ", imp_dat, self.now.strftime("%B"))
            if imp_dat > self.day :
                list_to_contact_final.append(0)
                list_contacted_final.append(0) 
            else:
                list_to_contact, list_contacted = [], []
                for owner in self.owners:
                    if owner.last_contact != None :
                        if owner.last_contact.contact_date + self.two_weeks > datetime(self.year, self.month, imp_dat).date():
                            list_contacted.append(owner)
                            continue
                    list_to_contact.append(owner)
                    continue
                print("à contacter : ", len(list_to_contact))
                print("contactés : ", len(list_contacted))
                list_to_contact_final.append(len(list_to_contact))
                list_contacted_final.append(len(list_contacted)) 
        print("FINAL")
        print("list_to_contact_final : ", list_to_contact_final)
        print("list_contacted_final : ", list_contacted_final)

        return self.now.strftime("%B %Y"), list_to_contact_final, list_contacted_final
    @property
    def get_list_for_search(self):
        """this function returns all the owners with caution"""
        print('start')
        list_to_contact, list_contacted = [], []
        for owner in self.owners: 
            if owner.last_contact:
                if owner.last_contact.contact_date + self.two_weeks > self.now:
                    list_contacted.append(owner)
                    continue 
            list_to_contact.append(owner)
        
        return self.owners, list_to_contact, list_contacted


    # def getPrevData(self):
    #     """
    #         returns a dict of actionable datas
    #     """
    #     queryset = GraModel.objects.all()
    #     prevData = {"contacted" : [], "to_contact": [], 'date': []}
    #     for gram in queryset:
    #         prevData['contacted'].append(gram.nb_contacted)
    #         prevData['to_contact'].append(gram.nb_to_contact)
    #         prevData['date'].append(gram.date.strftime("%d/%m/%y"))
    #     first_month = queryset[0].date.strftime("%d/%m/%y")
    #     last_month = queryset[len(queryset)-1].date.strftime("%d/%m/%y")
    #     prevData['month'] = f"Graphe du {first_month} au {last_month}"
    #     return prevData