# script full of useful functions for views.py
import json
from sheet.models import Animal, Owner, AdminData
from .models import Mail
from .data import converter
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

    def alter_db(self, dict_values, given_id): 
        dv2 = dict_values.copy()
        dv2.pop('csrfmiddlewaretoken', None)
        mail = Mail.objects.get(mail_id=given_id)
        for key in dv2: 
            setattr(mail, key, dv2[key])
            print(key, getattr(mail, key))
            print("********")
        mail.save()
        return mail

    def get_mail_from_id(self, mail_id):
        return Mail.objects.get(mail_id=mail_id)
    
    def modify_text(self, plain_text):
            """takes plain text and returns modified text"""
            print("plain_text from modify_text : ", plain_text)
            anim = Animal.objects.all()[0]
            species = ("0", "chat"),("1", "chatte"), ("2", "chien"), ("3", "chienne")
            ststatus = (0,"stérile"), (2,"stérilisable"), (3,"à stériliser")
            sex = (0, 'Monsieur'), (1, 'Madame')
            species_name = lambda x : species[int(x)][1]
            steril_status = lambda x : ststatus[int(x)][1]
            get_str_sex = lambda x : sex[int(x)][1]
            new_text = plain_text
            dict_conversion = converter(anim)
            for key in dict_conversion: 
                if key == '**date de stérilisation**':
                    pass
                    # print("before :")
                    # print(new_text)
                if dict_conversion[key] == "": 
                    dict_conversion[key] = f" {key} = vide"
                new_text = new_text.replace(key, dict_conversion[key])

            # print(new_text)
            new_text = new_text.replace('\r\n', '\\n')
            plain_text = plain_text.replace('\r\n', '\\n')
            return plain_text, new_text

    def change_auto_send(self, mail, num):
        if num == '0': 
            self.auto_send_false(mail)
            mail.auto_send=False
            mail.save()
        else:
            mail.auto_send=True
            mail.save()
        # print(f"changement auto_send pour {mail.auto_send}")

    def auto_send_false(self, mail):
        keys = 'send_after_creation','send_after_modif',
        for key in keys:
            setattr(mail, key, False)

        keys = 'send_when_x_month','send_at_this_date'
        for key in keys:
            setattr(mail, key, None)

    def drop_mail(self, given_id):
        """ this functions drops sheets in the db
            1/ find animal with given_id
            2/ drop animal and his AdminData (because it is unique)
            3/ checks whether the owner is connected to others animals
            4/ yes > doesn't drop it || no > drops it 
        """
        print("drop_mail", given_id)
        for elem in given_id:
            # print(f"Utils.drop_mail >> {elem}")
            mail = Mail.objects.get(mail_id=elem)
            # print(f"\tMail trouvé : {mail}")
            mail.delete()
            # print(f"\tMail supprimé.")
            