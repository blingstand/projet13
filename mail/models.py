#from python 
import datetime
import locale

#from django 
from django.db import models
from django.core.mail import send_mail

#from app
from mail.data import converter

#from other app
from sheet.models import Animal
# ut = Utils() 

locale.setlocale(locale.LC_TIME,'')
# Create your models here.
class Mail(models.Model):
    mail_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    resume = models.CharField(blank=True, max_length=120)
    plain_text = models.TextField(blank=True)
    auto_send = models.BooleanField(blank=True,default=False)
    send_after_creation = models.BooleanField(blank=True,default=False)
    send_after_delete = models.BooleanField(blank=True,default=False)
    send_after_modif = models.BooleanField(blank=True,default=False)
    send_when_x_month = models.IntegerField(blank=True,default=None, null=True)
    send_at_this_date = models.DateField(blank=True, default=None, null=True)

    def __str__(self):
        if self.mail_id is not None: 
            return f'mail{self.mail_id} (titre: {self.title})'
        return f'mail(titre: {self.title})'

    def get_condition(self): 
        #this function returns a condition(str) if auto_send = true, else returns None 
        condition = {
            self.send_after_creation : (bool, 'à la création de la fiche'),
            self.send_after_modif : (bool, 'à la modification de la fiche'),
            self.send_after_delete : (bool, 'à la supression de la fiche'),
            self.send_when_x_month : (int, f"pour les {self.send_when_x_month} mois de l'animal"),
            self.send_at_this_date : (datetime.datetime, f'à la date du {self.send_at_this_date}')}

        if self.auto_send == False: 
            return None
        for key in condition:
            if isinstance(key, condition[key][0]):
                if key == False:
                    continue
                return condition[key][1]
    @property
    def modified_text(self):
        """takes plain text and returns modified text"""
        anim = Animal.objects.all()[0]
        new_text = self.plain_text
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
        return new_text
    def full_text(self):
        """this function returns a plain text with escaped \n """
        return self.plain_text.replace('\r\n', '\\n')


    def send_auto_mail(self, send_to):
        """this function sends an auto mail according to its values and param """
        print("from send_auto_mail, I send to : ")
        print(send_to)
        send_mail(
            self.resume, self.modified_text, 'blingstand@hotmail.fr', 
            ['adrien.clupot@gmail.com'], fail_silently=False)
        print("send_auto_mail > mail send")

