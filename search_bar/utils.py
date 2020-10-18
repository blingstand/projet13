# from others app
from sheet.models import *

class Utils(): 

	def answering(self, input_value): 
		"""this function finds an answer to the input_value"""
		list_response=[]
		if len(input_value)< 6 :
			return "0"
		five_first = input_value[0:5]
		rest = input_value[5:].upper()
		
		if five_first == "prop:":
			owners = Owner.objects.filter(owner_surname__contains=rest).order_by('owner_surname')
			if owners:
				for owner in owners : 
					list_response.append({
						'id':owner.id, 
						'str':f"{owner.apostrophe} {owner.owner_surname} {owner.owner_name.capitalize()}"})
				return list_response
		
		elif five_first == "anim:":
			print("five_first > anims", five_first)
			anims = Animal.objects.filter(name__contains=rest).order_by('name')
			if anims:
				for anim in anims : 
					list_response.append({
						'id':anim.id, 
						'str':f"{anim.name} - puce{anim.admin_data.chip or ' xxx'}"})
				return list_response
		
		elif five_first == "puce:":
			print("five_first > anims", five_first)
			admins = AdminData.objects.filter(chip__contains=rest)
			if admins:
				for admin in admins : 
					anim = Animal.objects.get(admin_data=admin)
					list_response.append({
						'id':anim.id, 
						'str':f"{anim.name} - puce = {anim.admin_data.chip or 'xxx'}"})
				return list_response
		return "0"