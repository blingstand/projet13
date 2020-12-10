"""script full of useful functions for views.py"""
#from python
import locale

#from this app
from .models import Mail
locale.setlocale(locale.LC_TIME,'')
class UtilsMail():
    """ class full of usefull functions"""
    def save_datas(self,dict_values):
        """ creates and saves a mail"""
        new_mail = Mail(
            title=dict_values['title'],
            resume=dict_values['resume'],
            plain_text=dict_values['plain_text'])
        print("Utils.save_data : Voici ce que je vais enregistrer :")
        print(new_mail)
        new_mail.save()
        return new_mail.mail_id
    def alter_db(self, dict_values, given_id):
        """ modify a mail identified by its id """
        dv2 = dict_values.copy()
        dv2.pop('csrfmiddlewaretoken', None)
        mail = Mail.objects.get(mail_id=given_id)
        for key in dv2:
            setattr(mail, key, dv2[key])
        mail.save()
        return mail
    def get_mail_from_id(self, mail_id):
        """ returns an identified mail """
        return Mail.objects.get(mail_id=mail_id)
    
    def change_auto_send(self, mail, num):
        """adapt auto send value to param"""
        if num == '0':
            mail.auto_send=False
            mail.save()
        else:
            mail.auto_send=True
            mail.save()
        # print(f"changement auto_send pour {mail.auto_send}")

    def drop_mail(self, given_id):
        """ this functions drops mail from db"""
        print("drop_mail", given_id)
        for elem in given_id:
            # print(f"Utils.drop_mail >> {elem}")
            mail = Mail.objects.get(mail_id=elem)
            # print(f"\tMail trouvé : {mail}")
            mail.delete()
            # print(f"\tMail supprimé.")
