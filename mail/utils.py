# script full of useful functions for views.py
#from python 
import json
import locale

from .models import Mail

#from others app 
from sheet.models import Animal, Owner, AdminData


locale.setlocale(locale.LC_TIME,'')

class UtilsMail():
    """ class full of usefull functions"""
    def save_datas(self,dict_values):
        new_mail = Mail(
            title=dict_values['title'],
            resume=dict_values['resume'],
            plain_text=dict_values['plain_text'])
        print("Utils.save_data : Voici ce que je vais enregistrer :")
        print(new_mail)
        new_mail.save()
        return new_mail.mail_id

    def alter_db(self, dict_values, given_id): 
        print("alter db")
        dv2 = dict_values.copy()
        dv2.pop('csrfmiddlewaretoken', None)
        mail = Mail.objects.get(mail_id=given_id)
        for key in dv2: 
            setattr(mail, key, dv2[key])
            print(key, getattr(mail, key))
            print("********")
        mail.save()
        print(mail.modified_text)
        return mail

    def get_mail_from_id(self, mail_id):
        return Mail.objects.get(mail_id=mail_id)

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

    def has_to_send_mail(self, action, data):
        """ this function verifies whether a mail should be send according to the action """
        queryset = ""
        if action == 'creation': 
            queryset = Mail.objects.filter(auto_send=True, send_after_creation=True)
        elif action == 'modif': 
            queryset = Mail.objects.filter(auto_send=True, send_after_modif=True)
        elif action == 'delete': 
            print("action delete identifiée ")
            queryset = Mail.objects.filter(auto_send=True, send_after_delete=True)
            print(len(queryset))
        if len(queryset) > 0: 
            for ind, mail in enumerate(queryset):
                print(ind, mail)
                mail.send_auto_mail(data)

            