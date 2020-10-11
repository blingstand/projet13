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

    @property
    def get_list_datas(self):
    	""" this functions returns a list of dict. 
    	Each dict contains owner, date_of_adoption, last_contact
    	"""
    	list_datas = []
    	for anim in self.anim_with_caution:
    		new_dict = {}
    		owner = anim.owner
    		date_of_adoption = anim.date_of_adoption
    		contact = Contact.objects.filter(owner=owner)
    		if len(contact) > 0:
    			last_contact = contact[0].contact_date
    		elif len(contact) > 1:
    			last_contact = contact[-1].contact_date
    		else:
    			# print("******get_list_datas" )
    			# print(f"je vire {owner}, car il n'a pas de contact")
    			# print("******get_list_datas" )
    			continue
    		new_dict['owner'] = owner
    		new_dict['date_of_adoption'] = date_of_adoption
    		new_dict['to_contact'] = owner.to_contact
    		if len(list_datas) >= 1:
    			if not new_dict['owner'] in [dict_data['owner'] for dict_data in list_datas]:
    				list_datas.append(new_dict)
    		else:
    			list_datas.append(new_dict)
    	return list_datas
    @property
    def get_list_for_search(self):
    	"""this function returns all the owners with caution"""
    	datas = self.get_list_datas
    	list_owner, list_to_contact, list_contacted = [], [], []
    	for data in datas: 
    		if data["owner"] not in list_owner:
    			list_owner.append(data['owner'])
    			if data['owner'].to_contact:
    				list_to_contact.append(data['owner'])
    			else:
    				list_contacted.append(data['owner'])
    	return list_owner, list_to_contact, list_contacted


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