# from .models import Mail

from sheet.models import Animal, Owner, AdminData
from .models import Mail
import locale
locale.setlocale(locale.LC_TIME,'')
class Utils():
    """ class full of usefull functions"""
    def save_datas(self,dict_values):
        new_mail = Mail(
            title=dict_values['title'],
            resume=dict_values['resume'],
            full_text=dict_values['full_text'])
        print("Utils.save_data : Voici ce que je vais enregistrer :")
        print(new_mail)
        new_mail.save()
        return new_mail.mail_id

    def get_mail_from_id(self, mail_id):
        return Mail.objects.get(mail_id=mail_id)

    def change_date_format(self, date):
        """ take a date format and change it to a french date format """
        return date.strftime('%A %d %B %Y')
    def modify_text(self, text):
            """takes plain text and returns modified text"""
            print(f"texte à changer : {text}")
            anim = Animal.objects.all()[0]
            species = ("0", "chat"),("1", "chatte"), ("2", "chien"), ("3", "chienne")
            ststatus = (0,"stérile"), (2,"stérilisable"), (3,"à stériliser")
            sex = (0, 'Monsieur'), (1, 'Madame')
            species_name = lambda x : species[int(x)][1]
            steril_status = lambda x : ststatus[int(x)][1]
            get_str_sex = lambda x : sex[int(x)][1]
            input_output = {
                '**color**' : anim.color, 
                '**date_of_adoption**' : self.change_date_format(anim.date_of_adoption),
                '**futur_date_of_neuter**' : self.change_date_format(anim.admin_data.futur_date_of_neuter), 
                '**is_neutered**' : steril_status(anim.admin_data.is_neutered), 
                '**name**' : anim.name, 
                '**owner_name**' : anim.owner.owner_name, 
                '**owner_surname**' : anim.owner.owner_surname, 
                '**owner_sex**' : get_str_sex(anim.owner.owner_sex), 
                '**species**' : species_name(anim.species), 
                }
            for key in input_output : 
                text = text.replace(key, input_output[key])
            return(text)

