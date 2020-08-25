from .models import *

def get_animals_for_template():
    """ return a list easy to use for template, build with different models"""
    #1 get list
    #2 clé de tri and order up/down objects.all(order_by)


    animals = [animal for animal in Animal.objects.all()]
    all_sheets = []
    for a in animals:
        if a.admin_data.is_neutered:
            a.status = 'stérile'
        else:
            if a.admin_data.can_be_neutered:
                a.status = f'peut être stérilisé(e)'
            else: 
                a.status = f'ne peut pas encore être stérilisé(e)'
        if a.owner.mail_reminder > 2:
            a.owner_status = "oui"
        else:
            a.owner_status = "non"
        a.owner_name = f"{a.owner.owner.upper()}"
        a.admin_data.file = a.admin_data.file or "vide"
        a.admin_data.chip = a.admin_data.chip or "vide"
        a.admin_data.tatoo = a.admin_data.tatoo or "vide"
        print(f"--\n> nom : {a.name}\nid : {a.animal_id}\nnature : {a.species}\nstatut : {a.status}"\
            f"\nrace : {a.race}\npropriétaire : {a.owner}\nstatut propriétaire : {a.owner_status}"\
            f"\ntel propriétaire : {a.owner.phone}"\
            f"\nnum dossier : {a.admin_data.file}"\
            f"\nnum tatouage : {a.admin_data.tatoo}"\
            f"\nnum puce : {a.admin_data.chip}")

        all_sheets.append(a)
    return all_sheets

