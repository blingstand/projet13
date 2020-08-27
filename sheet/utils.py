from .models import *

def get_animals_for_template():
    """ return a list easy to use for template, build with different models"""
    #1 get list
    #2 clé de tri and order up/down objects.all(order_by)
    animals = [animal for animal in Animal.objects.all()]
    all_sheets = []
    for a in animals:
        print(a)
        if a.admin_data.is_neutered:
            a.status = 'stérile'
        else:
            if a.admin_data.can_be_neutered:
                a.status = f'peut être stérilisé(e)'
            else: 
                a.status = f'ne peut pas encore être stérilisé(e)'
        try:
            a.owner_name = f"{a.owner.owner.upper()}"
            a.admin_data.file = a.admin_data.file or "vide"
            a.admin_data.chip = a.admin_data.chip or "vide"
            a.admin_data.tatoo = a.admin_data.tatoo or "vide"
            print(f"--\n> nom : {a.name}\nid : {a.animal_id}\nnature : {a.species}\nstatut : {a.status}"\
                f"\nrace : {a.race}\npropriétaire : {a.owner}"\
                f"\ntel propriétaire : {a.owner.phone}"\
                f"\nnum dossier : {a.admin_data.file}"\
                f"\nnum tatouage : {a.admin_data.tatoo}"\
                f"\nnum puce : {a.admin_data.chip}")
            all_sheets.append(a)

            
        except Exception as e:
            raise e
    return all_sheets

def get_animal_from_given_id(given_id):
    animal = Animal.objects.filter(animal_id=given_id)
    return animal 
