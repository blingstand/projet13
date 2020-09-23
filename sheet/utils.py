from .models import *
import datetime
class Utils():
    def get_animals_for_template(self):
        """ return a list easy to use for template, build with different models"""
        #1 get list of animals
        animals = [animal for animal in Animal.objects.all()]
        all_sheets = []
        species = ("0", "chat"),("1", "chatte"), ("2", "chien"), ("3", "chienne")
        ststatus = (0,"stérile"), (2,"stérilisable"), (3,"sera stérilisable")

        species_name = lambda x : species[int(x)][1]
        steril_status = lambda x : ststatus[int(x)][1]
        for a in animals:
            a.species = species_name(a.species)
            a.owner.owner_surname, a.owner.owner_name = a.owner.owner_surname.upper(), a.owner.owner_name.upper()
            a.admin_data.is_neutered = steril_status(a.admin_data.is_neutered)
            if a.admin_data.is_neutered == 'sera stérilisable': 
                a.admin_data.is_neutered = f'sera stérilisable le {a.admin_data.futur_date_of_neuter}'
            try:
                a.admin_data.file = a.admin_data.file or "vide"
                a.admin_data.chip = a.admin_data.chip or "vide"
                a.admin_data.tatoo = a.admin_data.tatoo or "vide"
                all_sheets.append(a)
                # print(f"--\n> nom : {a.name}\nid : {a.animal_id}\nnature : {a.species}\nstatut : {a.status}"\
                #     f"\nrace : {a.race}\npropriétaire : {a.owner}"\
                #     f"\ntel propriétaire : {a.owner.phone}"\
                #     f"\nnum dossier : {a.admin_data.file}"\
                #     f"\nnum tatouage : {a.admin_data.tatoo}"\
                #     f"\nnum puce : {a.admin_data.chip}") 
            except Exception as e:
                raise e
        return all_sheets
    def get_animal_from_given_id(self, given_id):
        animal = Animal.objects.filter(animal_id=given_id)
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
            animal = Animal.objects.get(animal_id=elem)
            admin = animal.admin_data
            owner = animal.owner
            print(animal, ' || ', admin, ' || ', owner)
            other_animal = Animal.objects.filter(owner=owner)
            print(len(other_animal) , other_animal)
            animal.delete()
            admin.delete()
            if len(other_animal) - 1 == 0 :
                owner.delete()
                print(f"Suppression de : {animal}, {admin} et {owner}")
                continue
            print(f"/!\ Atention ce propriétaire a plusieurs animaux, seuls les fiches {animal} et {admin}"\
                    " seront effacées.")
    def change_date_format(self, dict_values):
        """ 
            this function turns str date into datetime.date
        """    
        format_str = '%d/%m/%Y' # The format
        for date in ('date_of_birth', 'date_of_adoption', 'date_of_neuter', 'futur_date_of_neuter'):
            if dict_values[date] != "": 
                dict_values[date] = datetime.datetime.strptime(dict_values[date], format_str).date()
            else:
                dict_values[date] = None
        return dict_values

    def find_changes(self, given_id, dict_values):
        """ this funtions makes a comparison between db class datas and dict_values datas
            if it finds a changes, this one is add to list changes 

        """
        # 1/  finds the concerned tables
        animal = Animal.objects.get(animal_id=given_id)
        # print("la modif concerne : ", animal, animal.admin_data, animal.owner)
        #2/ finds difference between former and new datas
        loop_animal = ('name', 'date_of_birth', 'race', 'species', 'color', 'date_of_adoption', 'observation'), animal
        loop_admin = ('file', 'chip', 'tatoo', 'is_neutered', 'date_of_neuter', 'futur_date_of_neuter', 'status'), animal.admin_data
        loop_owner = ('owner_name', 'owner_surname','owner_sex',  'phone', 'mail', 'tel_reminder', \
            'mail_reminder', 'caution'), animal.owner
        loop = [loop_animal, loop_admin, loop_owner]
        changes = []
        dict_values = self.change_date_format(dict_values)
        for elem in loop:
            for key in elem[0]: 
                if getattr(elem[1], key) != dict_values[key]:
                    changes.append((key, elem[1]))
        print("liste des modifications : ", changes)
        return changes

    def modify_datas(self, given_id, dict_values):
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
        animal = Animal.objects.get(animal_id=given_id)
        is_same_owner = (dict_values['former_owner'] == str(animal.owner.id))
        # print("==========")
        # print((dict_values['former_owner'], animal.owner.id))
        # print(f'is_same_owner : {is_same_owner}')
        # print("==========")
        
        try:
            if not is_same_owner and int(dict_values['former_owner']) > 0:
                # print("Cas 1 : Je change l'animal de propriétaire.")
                animal.owner = Owner.objects.get(id=dict_values['former_owner'])
                animal.save()
            elif not is_same_owner and int(dict_values['former_owner']) == 0:
                # print("Cas 2 : J'attribue à l'animal un nouveau propriétaire.")
                new_owner = Owner(
                    owner_name=dict_values['owner_name'],
                    owner_surname=dict_values['owner_surname'],
                    owner_sex=dict_values['owner_sex'],
                    phone=dict_values['phone'],
                    mail=dict_values['mail'],
                    tel_reminder=dict_values['tel_reminder'],
                    mail_reminder=dict_values['mail_reminder'],
                    caution=dict_values['caution']
                    )
                new_owner.save()
                animal.owner = new_owner
                animal.save()
                # print(f"\taprès > {animal.owner}")
            else:
                print(f'Cas3 : Je garde le même propriétaire {animal.owner}.')
            
            #I search for changes
            changes = self.find_changes(given_id, dict_values)
            allchanges = changes
            print(changes)
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
            # print("---> fin de la modif")
            #if animal is neutered so owner has no obligation
            if animal.admin_data.is_neutered == "0": 
                animal.owner.need_contact = False
            else: 
                animal.owner.need_contact = True
            owner = animal.owner
            owner.save()
            # print(f"Besoin de contacter {owner} pour stérilisation : {owner.need_contact}")
            #sum up
            # print(f'> {len(allchanges)} changement(s) détectés et effectués :')
            # [print(change) for change in allchanges]
            return True, len(allchanges)
        except Exception as e:
            return False, e

    def remove_owner(self, given_ids): 
        """this function removes 1 owner from db if the ctrl is ok"""
        if isinstance(given_ids, int): 
            given_ids = list(given_ids)
        for given_id in given_ids:
            owner_to_remove = Owner.objects.get(id=given_id)
            if owner_to_remove.number_animal() == 0: 
                owner_to_remove.delete()
            else:
                return False, f"{owner_to_remove} n'a pas été effacé(e) car il possède au moins un animal." 
        return True, f'Le(s) {len(given_ids)} propriétaire(s) a/ont été effacé(s).'

    def check_owner_values(self, dict_values, given_id=None, for_modif=None):
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

    def create_owner(self, dict_values):
        """this function creates a new owner if it is possible """
        try:
            success, message = self.check_owner_values(dict_values)
            if success:
                ow = Owner(
                    owner_name=dict_values['owner_name'],
                    owner_surname=dict_values['owner_surname'],
                    owner_sex=dict_values['owner_sex'],
                    phone=dict_values['phone'],
                    mail=dict_values['mail'],
                    mail_reminder=dict_values['mail_reminder'],
                    tel_reminder=dict_values['tel_reminder'],
                    caution=dict_values['caution'])
                ow.save()
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
                    owner.save()
                return True, "Modifications effectuées."
            else: 
                return success, message
        except Exception as e:
            # return False, f"une erreur a été rencontrée : {e}"
            raise e