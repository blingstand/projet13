def change_date_format(date):
        """ take a date format and change it to a french date format """
        if date is not None: 
            return date.strftime('%A %d %B %Y')
        return ""


def converter_data(anim):     
    converter = {
            '**caution**' : f'{anim.caution}€', 
            '**caution totale**' : f'{anim.owner.sum_caution}€', 
            '**couleur**' : f'couleur : {anim.color}', 
            "**date d'adoption**" : change_date_format(anim.date_of_adoption),
            '**date de naissance**' : change_date_format(anim.date_of_birth),
            '**date de stérilisation**' : change_date_format(anim.admin_data.date_of_neuter),
            '**date future stérilisation**' : change_date_format(anim.admin_data.futur_date_of_neuter), 
            '**espèce**' : anim.str_species, 
            '**état stérilisation**' : anim.admin_data.neuter_status, 
            '**id dossier**' : anim.admin_data.file, 
            '**id puce**' : anim.admin_data.chip, 
            '**id tatouage**' : anim.admin_data.tatoo, 
            '**M./Mme**' : anim.owner.apostrophe, 
            '**mail**' : anim.owner.mail, 
            '**nb appels**' : f'{anim.owner.tel_reminder} appel(s)', 
            '**nb mails**' : f'{anim.owner.mail_reminder} mail(s)', 
            '**nom animal**' : anim.name, 
            '**nom prop**' : anim.owner.owner_surname.upper(), 
            '**prénom prop**' : anim.owner.owner_name.capitalize(), 
            '**tel**' : anim.owner.phone, 
            '**race**' : f'race : {anim.race}', 
            } 
    return converter

options_animal = (
    { "content" : "**nom animal**", "visible": "nom"},
    { "content" : "**date de naissance**", "visible": "date de naissance"},
    { "content" : "**race**", "visible": "race"},
    { "content" : "**espèce**", "visible": "espèce"},
    { "content" : "**couleur**", "visible": "couleur"},
    { "content" : "**date d'adoption**", "visible": "date d'adoption"},
    { "content" : "**caution**", "visible": "caution"},
    )
options_owner = (
    { "content" : "**M./Mme**", "visible" : "M./Mme" }, 
    { "content" : "**nom prop**", "visible" : "nom propriétaire" }, 
    { "content" : "**prénom prop**", "visible" : "prénom propriétaire" }, 
    { "content" : "**tel**", "visible" : "téléphone" }, 
    { "content" : "**caution totale**", "visible" : "caution totale" }, 
    { "content" : "**mail**", "visible" : "mail" }, 
    { "content" : "**nb appels**", "visible" : "nombre d'appels" }, 
    { "content" : "**nb mails**", "visible" : "nombre de mails" }, 
    )
options_admin = (
   { "content" : "**id dossier**", "visible" : "id dossier" },
   { "content" : "**id puce**", "visible" : "id puce" },
   { "content" : "**id tatouage**", "visible" : "id tatouage" },
   { "content" : "**état stérilisation**", "visible" : "état stérilisation" },
   { "content" : "**date de stérilisation**", "visible" : "date de stérilisation" },
   { "content" : "**date future stérilisation**", "visible" : "futur date stérilisation" },
    )