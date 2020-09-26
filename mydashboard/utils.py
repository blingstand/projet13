# from django.db import models

# from .models import GraModel


# #from other apps
# from sheet.models import Owner, Animal

# # Create your models here.
# class GraphDatas():
#     """ All the datas that graph needs to be built """
#     def __init__(self):
#         self.list_owner = self.get_owner()
#         self.nb_owner_with_obligations = len(self.list_owner)
#         self.contacted, self.to_contact, self.list_owner = self.get_report()

#     def get_owner(self): 
#         """ this function returns  :
#                 > owner with obligation
#                 > """ 
#         owner_with_obligations = Owner.objects.filter(need_contact=True)
#         list_owner = []
#         for owner in owner_with_obligations: 
#         	# print(owner, owner in list_owner, len(list_owner))
#         	if owner not in list_owner: 
#         		list_owner.append(owner)
#         # print("***")
#         return  list_owner

#     def get_report(self):
#         """ This functions returns the number of owner with same number of mail 
#         and tel contact if this number is not 0 
#         """
#         # print("get_report")
#         all_owner_contacted = []
#         all_owner_to_contact = []
#         for owner in self.list_owner:

#             if owner.mail_reminder == 0:
#                 pass
#             if int(owner.mail_reminder) > 0 and int(owner.mail_reminder) == int(owner.tel_reminder):
#                 # print("all_owner_contacted + 1")
#                 all_owner_contacted.append(owner)
#             elif int(owner.mail_reminder) > 0 and int(owner.mail_reminder) > int(owner.tel_reminder):
#                 # print("all_owner_to_contact + 1")
#                 all_owner_to_contact.append(owner)
#         # print('tous, à contacter, contactés')
#         # print(len(all_owner_contacted), len(all_owner_to_contact), (all_owner_to_contact))
#         return (len(all_owner_contacted), len(all_owner_to_contact), all_owner_to_contact)

#     def getPrevData(self):
#         """
#             returns a dict of actionable datas
#         """
#         queryset = GraModel.objects.all()
#         prevData = {"contacted" : [], "to_contact": [], 'date': []}
#         for gram in queryset:
#             prevData['contacted'].append(gram.nb_contacted)
#             prevData['to_contact'].append(gram.nb_to_contact)
#             prevData['date'].append(gram.date.strftime("%d/%m/%y"))
#         first_month = queryset[0].date.strftime("%d/%m/%y")
#         last_month = queryset[len(queryset)-1].date.strftime("%d/%m/%y")
#         prevData['month'] = f"Graphe du {first_month} au {last_month}"
#         return prevData