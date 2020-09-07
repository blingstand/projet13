from .models import *

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
            print(a.name, a.admin_data.is_neutered)
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