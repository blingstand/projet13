from .models import *

def get_animals_for_template():
    """ return a list easy to use for template, build with different models"""
    #1 get list of animals
    animals = [animal for animal in Animal.objects.all()]
    all_sheets = []
    for a in animals:
        a.owner.owner_surname, a.owner.owner_name = a.owner.owner_surname.upper(), a.owner.owner_name.upper()
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

def get_animal_from_given_id(given_id):
    animal = Animal.objects.filter(animal_id=given_id)
    return animal 
