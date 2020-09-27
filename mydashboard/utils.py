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
    			continue
    		new_dict['owner'] = owner
    		new_dict['date_of_adoption'] = date_of_adoption
    		new_dict['last_contact'] = last_contact
    		list_datas.append(new_dict)
    	return list_datas

    @property
    def contacted_or_to_contact(self):
    	"""this functions reads get_list_datas and return a list of each owner
    	who has been contacted less than 7 days before"""
    	self.contacted, self.to_contact = [], []
    	list_datas = self.get_list_datas
    	now = datetime.now().date()
    	print("***contacted_or_to_contact")
    	for dict_datas in list_datas:
    		last_contact = dict_datas['last_contact']
    		more_than_a_week = (now - timedelta(weeks=1)) >= last_contact
    		print((now - timedelta(weeks=1)) >= last_contact, (now - timedelta(weeks=1))," >= ", last_contact)
    		if more_than_a_week:
    			self.to_contact.append(dict_datas)
    		else:
    			self.to_contact.append(dict_datas)

    	print("contacted_or_to_contact***")
    	return self.contacted, self.to_contact
    




    def get_report(self):
        """ This functions returns the number of owner with same number of mail 
        and tel contact if this number is not 0 
        """
        # print("get_report")
        all_owner_contacted = []
        all_owner_to_contact = []
        for owner in self.owner_with_obligations:
            if owner.mail_reminder == 0:
                pass
            if int(owner.mail_reminder) > 0 and int(owner.mail_reminder) == int(owner.tel_reminder):
                # print("all_owner_contacted + 1")
                all_owner_contacted.append(owner)
            elif int(owner.mail_reminder) > 0 and int(owner.mail_reminder) > int(owner.tel_reminder):
                # print("all_owner_to_contact + 1")
                all_owner_to_contact.append(owner)
        # print('tous, à contacter, contactés')
        # print(len(all_owner_contacted), len(all_owner_to_contact), (all_owner_to_contact))
        return (len(all_owner_contacted), len(all_owner_to_contact), all_owner_to_contact)

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