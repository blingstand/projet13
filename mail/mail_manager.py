"""script that manages the sending mail function """
#from python
from datetime import datetime
#from other app
from sheet.models import Contact
#from this app
from .models import Mail

class MailManager():
    """this class sends mail and keep a trace in db """
    def refresh_reminder(self, owner):
        """ this function refresh data for mail_reminder and tel reminder """
        owner.refresh_sum_mail
        owner.refresh_sum_tel
    def create_contact(self, owner, dict_values):
        """this function creates a new contact for a owner """
        print('create_contact')
        try:
            new_contact = Contact(
                contact_date = dict_values['contact_date'],
                resume = dict_values['resume'],
                full_text = dict_values['full_text'],
                nature = dict_values['nature'],
                owner = owner)
            new_contact.save()
            # print("je crée un contact pour ", owner,\
            #     f"({owner.mail_reminder} || {owner.tel_reminder})")
            self.refresh_reminder(owner)
            # print("et j'actualise ", owner,\
            #     f"({owner.mail_reminder} || {owner.tel_reminder})")
            return True, new_contact
        except Exception as exc:
            # raise(exc)
            return False, f"problème pour ut.create_contact: {exc}"
    def send_and_trace(self, given_id, list_mail, list_owner):
        """this functions sends a mail and keep a trace in base """
        print("send_and_trace")
        dict_datas = { "contact_date" : datetime.now().date(),
        "resume" : "","full_text" : "","nature" : "5"}
        for mail in list_mail:
            dict_datas['resume'] = mail.title
            dict_datas['full_text'] = mail.modified_text(given_id)
            for owner in list_owner :
                mail.send_auto_mail(owner, given_id)
                self.create_contact(owner, dict_datas)
    def has_to_send_mail(self, action, list_owner, given_id):
        """ this function verifies, send and trace
        verifies whether a mail should be send according to parameters
        """
        # print("has_to_send_mail")
        list_mail = ""
        if action == 'creation':
            list_mail = Mail.objects.filter(auto_send=True, send_after_creation=True)
        elif action == 'modif':
            list_mail = Mail.objects.filter(auto_send=True, send_after_modif=True)
        elif action == 'delete':
            list_mail = Mail.objects.filter(auto_send=True, send_after_delete=True)
        # print("has_to_send_mail : ", len(list_mail), " trouvé")
        # print("pour l'animal de cet id : ", given_id)
        if len(list_mail) > 0:
            self.send_and_trace(given_id, list_mail, list_owner)
