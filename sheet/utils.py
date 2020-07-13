from .models import *

def get_animals_for_template():
    """ return a list easy to use for template, build with different models"""
    #1 get list
    #2 clé de tri and order up/down objects.all(order_by)


    list_animals = [animal for animal in Animal.objects.all()]
    animals = []
    for a in list_animals:
        if a.admin_data_id.is_neutered:
            a.status = 'stérile'
        else:
            if a.admin_data_id.can_be_neutered:
                a.status = f'peut être stérilisé(e)'
            else: 
                a.status = f'ne peut pas encore être stérilisé(e)'
        if a.owner_id.mail_reminder > 2:
            a.owner_status = "oui"
        else:
            a.owner_status = "non"
        a.owner = f"{a.owner_id.owner.upper()}"
        print(f"--\n> nom : {a.name}\nnature {a.species}\nstatut : {a.status}"\
            f"\nrace : {a.race}\npropriétaire : {a.owner}\nstatut propriétaire : {a.owner_status}"\
            f"\ntel propriétaire : {a.owner_id.telephone}"\
            f"\nnum dossier : {a.admin_data_id.file}"\
            f"\nnum tatouage : {a.admin_data_id.tatoo}"\
            f"\nnum puce : {a.admin_data_id.chip}")
        animals.append(a)
    return animals

