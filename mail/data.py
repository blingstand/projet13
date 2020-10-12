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
            '**espèce**' : anim.str_species, 
            '**date future stérilisation**' : change_date_format(anim.admin_data.futur_date_of_neuter), 
            '**id dossier**' : anim.admin_data.file, 
            '**id puce**' : anim.admin_data.chip, 
            '**id tatouage**' : anim.admin_data.tatoo, 
            '**état stérilisation**' : anim.admin_data.neuter_status, 
            '**nom animal**' : anim.name, 
            '**M./Mme**' : anim.owner.apostrophe, 
            '**mail**' : anim.owner.mail, 
            '**nb appels**' : f'{anim.owner.tel_reminder} appel(s)', 
            '**nb mails**' : f'{anim.owner.mail_reminder} mail(s)', 
            '**nom prop**' : anim.owner.owner_surname.upper(), 
            '**prénom prop**' : anim.owner.owner_name.capitalize(), 
            '**tel**' : anim.owner.phone, 
            '**race**' : f'race : {anim.race}', 
            }
    return converter