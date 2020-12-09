# from others app
from sheet.models import *

class Utils(): 

    def get_prop_answer(self, rest):
        owners = Owner.objects.all()
        owner_list = [ {'str': str(owner), 'id': owner.id} for owner in owners]
        given_value = rest.upper()
        list_candidates = []
        for owner in owner_list:
            if given_value in owner['str'].upper(): 
                print(given_value in owner['str'].upper(), given_value,  owner['str'].upper())
                list_candidates.append(owner)
                if len(list_candidates) >= 4:
                    return list_candidates
        return list_candidates
        # owners = Owner.objects.filter(owner_surname__contains=rest).order_by('owner_surname')
        # if owners:
        #   for owner in owners : 
        #       list_response.append({
        #           'id':owner.id, 
        #           'str':f"{owner.small_apostrophe} {owner.owner_surname} {owner.owner_name.capitalize()}"})
        #   return list_response
        # return "0"

    def answering(self, input_value): 
        """this function finds an answer to the input_value"""
        list_response=[]
        if len(input_value) < 6 :
            return []
        
        five_first = input_value[0:5]
        rest = input_value[5:].upper()
        
        if five_first == "prop:":
            return self.get_prop_answer(rest)
        
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