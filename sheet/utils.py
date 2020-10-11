#from python
from .models import *
import datetime

#from current app 
from .models import *

#from others apps
from mail.utils import UtilsMail
from mail.mail_manager import MailManager



mm = MailManager()
utm = UtilsMail()

class UtilsSheet():

    def get_data_for_alter(self, given_id):
        """this function return a dict values for altersheet from a given id"""
        anim = Animal.objects.get(id=given_id)
        data = {
            'caution' : anim.caution, 
            'chip' : anim.admin_data.chip, 
            'color' : anim.color, 
            'date_of_adoption' : str(anim.date_of_adoption), 
            'date_of_birth' : str(anim.date_of_birth), 
            'date_of_neuter' : str(anim.admin_data.date_of_neuter), 
            'futur_date_of_neuter' : str(anim.admin_data.futur_date_of_neuter), 
            "file" : anim.admin_data.file,
            "is_neutered" : anim.admin_data.is_neutered,
            "select_owner" : anim.owner.id,
            "mail" : anim.owner.mail,
            "name" : anim.name,
            "nature_caution" : anim.nature_caution,
            "status" : anim.admin_data.status,
            "owner_name" : anim.owner.owner_name,
            "owner_surname" : anim.owner.owner_surname,
            "owner_sex" : anim.owner.owner_sex,
            "phone" : anim.owner.phone,
            "race" : anim.race,
            "species" : anim.species,
            "tatoo" : anim.admin_data.tatoo}
        return data

    def get_animal_from_given_id(self, given_id):
        animal = Animal.objects.filter(id=given_id)
        return animal 
    def drop_sheet(self, given_id):
        """ this functions drops sheets in the db
            1/ find animal with given_id
            2/ drop animal and his AdminData (because it is unique)
            3/ checks whether the owner is connected to others animals
            4/ yes > doesn't drop it || no > drops it 
        """
        for elem in given_id:
            print(f">> {elem}")
            animal = Animal.objects.get(id=elem)
            admin, owner = animal.admin_data, animal.owner
            print(animal, ' || ', admin, ' || ', owner)
            other_animal = Animal.objects.filter(owner=owner)
            print(f"Ce propriétaire possède {len(other_animal)} animaux)")
            mm.has_to_send_mail("delete", [owner], animal.id)
            animal.delete()
            admin.delete()
            if len(other_animal) < 1 :
                owner.delete()
                print(f"Suppression de : {animal}, {admin} et {owner}")
                return
            print(f"/!\ Atention ce propriétaire a plusieurs animaux, seuls les fiches {animal} et {admin}"\
                    " seront effacées.")

    def change_date_format(self, dict_values):
        """ 
            this function turns str date into datetime.date
        """    
        format_str = '%Y-%m-%d' # The format
        list_data = ['date_of_birth', 'date_of_adoption']
        for key in ('date_of_neuter', 'futur_date_of_neuter'): 
            if key in dict_values: 
                list_data.append(key)
        for date in list_data:
            if dict_values[date] != "": 
                dict_values[date] = datetime.strptime(dict_values[date], '%Y-%m-%d').date()
            else:
                dict_values[date] = None
        return dict_values
    def get_choice_new_owner(self, owners): 
        """this function returns the choice new owner tupple"""
        owners = owners.order_by('owner_surname')
        choice_new_owner = [("0", "-- Nouveau Propriétaire --")]
        for owner in owners:
            choice = (str(owner.id), f"{owner.apostrophe} {owner.owner_surname.capitalize()} \
                {owner.owner_name.capitalize()} (id={owner.id})")
            choice_new_owner.append(choice)
        return tuple(choice_new_owner)
    def find_changes(self, given_id, dict_values):
        """ this funtions returns a list of changes 
            1/ it makes a comparison between db class datas and dict_values datas
            2/ if it finds a changes, this one is add to list of changes 

        """
        # 1/  finds the concerned tables
        animal = Animal.objects.get(id=given_id)
        # print("la modif concerne : ", animal, animal.admin_data, animal.owner)
        #2/ finds difference between former and new datas
        loop_animal = ('name', 'date_of_birth', 'race', 'species', 'color', 'date_of_adoption',\
          'caution',  'nature_caution'), animal
        loop_admin = ('file', 'chip', 'tatoo', 'is_neutered', 'date_of_neuter', 'futur_date_of_neuter',\
         'status'), animal.admin_data
        loop = [loop_animal, loop_admin]
        changes = []
        dict_values = self.change_date_format(dict_values)
        for elem in loop:
            for key in elem[0]: 
                if key not in dict_values:
                    dict_values[key]=None
                if getattr(elem[1], key) != dict_values[key]:
                    print(getattr(elem[1], key) != dict_values[key], type(getattr(elem[1], key)),  type(dict_values[key]))
                    print(getattr(elem[1], key) != dict_values[key], getattr(elem[1], key),  dict_values[key])
                    changes.append((key, elem[1]))
        print("liste des modifications : ", changes)
        return changes
    def change_animal_owner(self, animal, given_id):
        """this function modifies the animal.owner and returns the new_owner"""
        former_owner = animal.owner
        animal.owner = Owner.objects.get(id=given_id)
        new_owner = animal.owner
        if former_owner != new_owner: 
            animal.save()
            return new_owner
        else:
            raise "Erreur dans sheet.utils.py ligne 92"
    def modify_datas(self, changes, animal, dict_values):
        """this functions modifies the data according to change and dict_values"""
        try:    
            for change in changes:
                if change[1] == animal.owner: 
                    setattr(animal.owner, str(change[0]), dict_values[change[0]])
                    animal.owner.save()
                elif change[1] == animal.admin_data:
                    setattr(animal.admin_data, str(change[0]), dict_values[change[0]])
                    animal.admin_data.save()
                else:
                    setattr(animal, str(change[0]), dict_values[change[0]])
                    animal.save()
        except Exception as e:
            return False, e
    def manage_modify_datas(self, given_id, dict_values):
        """ this function attemps to modify the db 
            1/ determinates wehther we have a new owner for animal from given_id
                cas 1>changes for former owner : 
                    changes animal.owner
                cas 2>changes for new owner : 
                    creates owner, 
                    adds values, 
                    saves it, 
                    links to animal, 
                    saves animal
                cas 3>remain former owner
            2/ gets the changes to make
            3/ makes changes
        """
        # try:

        animal = Animal.objects.get(id=given_id)
        is_same_owner = (dict_values['select_owner'] == str(animal.owner.id))
        if not is_same_owner:
            former_owner = animal.owner
            if int(dict_values['select_owner']) > 0:
                new_owner = self.change_animal_owner(animal, dict_values['select_owner'])
            elif int(dict_values['select_owner']) == 0:
                # print("Cas 2 : J'attribue à l'animal un nouveau propriétaire.")
                new_owner = self.create_owner(dict_values, return_owner=True)
                animal.owner = new_owner
                animal.save()
        #I search for changes
        changes = self.find_changes(given_id, dict_values)
        self.modify_datas(changes, animal, dict_values)
        can_send_mail = False
        if is_same_owner: 
            for change in changes:
                print("change > ", change[0])
                if change[0] == "caution": 
                    can_send_mail = True
                    datas = [animal.owner]
        else:
            can_send_mail = True
            datas = [former_owner,new_owner]
        if can_send_mail: 
            print(can_send_mail)
            list_dict_datas = mm.has_to_send_mail("modif", datas, given_id)
            print("> mail envoyé : ", len(datas))
        return True, changes
        # except Exception as e:
        #     raise e
        #     return False, e

    
    """ methodes for Owner """
    def remove_owner(self, given_ids): 
        """this function removes 1 owner from db if the ctrl is ok"""
        if not isinstance(given_ids, list): 
            given_ids = [given_ids]
        for given_id in given_ids:
            owner_to_remove = Owner.objects.get(id=given_id)
            if owner_to_remove.number_animal() == 0: 
                owner_to_remove.delete()
            else:
                return False, f"{owner_to_remove} n'a pas été effacé(e) car il possède au moins un animal." 
        return True, f'{len(given_ids)} propriétaire(s) a/ont été effacé(s).'
    
    def check_owner_values(self, dict_values, given_id=None, for_modif=None):
        """ this function verifies the Integrity of data """
        queryset1 = Owner.objects.filter(
            phone=dict_values['phone'])
        queryset2 = Owner.objects.filter(
            mail=dict_values['mail'])
        if len(queryset1) != 0 and not for_modif: 
            return False, 'Ce numéro de téléphone existe déjà'
        elif len(queryset1) != 0 and for_modif:
            verif = (queryset1[0].id == given_id)
            if not verif:
                return False, 'Ce numéro de téléphone existe déjà'
        if len(queryset2) != 0 and not for_modif: 
            return False, 'Ce mail existe déjà'
        elif len(queryset2) != 0 and for_modif:
            verif = (queryset2[0].id == given_id)
            if not verif:
                return False, 'Ce mail existe déjà'
        return True, "aucun problème"
    def create_owner(self, dict_values, return_owner=False):
        """this function creates a new owner if it is possible """
        try:
            success, message = self.check_owner_values(dict_values)
            if success:
                ow = Owner(
                    owner_name=dict_values['owner_name'],
                    owner_surname=dict_values['owner_surname'].upper(),
                    owner_sex=dict_values['owner_sex'],
                    phone=dict_values['phone'],
                    mail=dict_values['mail'])
                ow.save()
                if return_owner: 
                    return owner
                return True, f"création de {ow.owner_name} réussie"
            else: 
                return success, message
        except Exception as e:
            return False, f"une erreur a été rencontrée : {e}"
            # raise e
    def modify_owner(self, given_id, dict_values):
        """this function modifies the recognize owner with dict_values """
        owner = Owner.objects.get(id=given_id)
        try:
            success, message = self.check_owner_values(dict_values, given_id, for_modif=True)
            if success:
                for key in dict_values: 
                    setattr(owner, key, dict_values[key])
                    owner.owner_surname = owner.owner_surname.upper()
                    owner.save()
                return True, "Modifications effectuées."
            else: 
                return success, message
        except Exception as e:
            # return False, f"une erreur a été rencontrée : {e}"
            raise 
    
    """ methodes for Contact """
    def remove_contact(self, list_contact_id):
        """this function identifies contact to remove and remove it """
        try:
            for given_id in list_contact_id:
                contact = Contact.objects.get(id=given_id)
                contact.delete()
            mm.refresh_reminder(contact.owner)
            return True, f"{contact} a été supprimé."
        except Exception as e:
            return False, f"ut.remove_contact > pas de supression car :\n{e}"
    def modify_contact(self, dict_values): 
        """ this function gets a selected contact and modifies its datas """
        try:
            selected_contact = Contact.objects.get(id=dict_values['id_modif'])
            del dict_values['id_modif']
            for key in dict_values:
                setattr(selected_contact, key, dict_values[key])
                selected_contact.save()
                mm.refresh_reminder(selected_contact.owner)
            return True, f"{selected_contact} a bien été modifié."
        except Exception as e:
            return False, f"modify_contact > problème ici : {e}"