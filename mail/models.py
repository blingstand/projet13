#from python 
import datetime
import locale

#from django 
from django.db import models
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

#from app
from mail.data import converter_data

#from other app
from sheet.models import *
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
    send_every_2_weeks = models.BooleanField(blank=True,default=False)
    send_when_neuterable = models.BooleanField(blank=True,default=False)

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
            self.send_when_neuterable : (bool, 'à la supression de la fiche'),
            self.send_every_2_weeks : (bool, 'à la supression de la fiche')}

        if self.auto_send == False: 
            return None
        for key in condition:
            if isinstance(key, condition[key][0]):
                if key == False:
                    continue
                return condition[key][1]
    
    def _get_false_animal(self):
        """this function returns a fictif animal in order to display an overview"""
        already_exists = Animal.objects.filter(name="patatin")
        if len(already_exists)==0: 
            admin = AdminData(
                file="filexxx", 
                chip="chipxxx", 
                tatoo="tatooxxx",
                is_neutered= "0",
                date_of_neuter= datetime(2020,1,2).date(),
                futur_date_of_neuter= datetime(2021,1,2).date())
            owner = Owner(
                owner_name = 'pierre',
                owner_surname = 'dupont',
                owner_sex = "0",
                phone = '1234567890',
                mail = 'pd@mail.com')

            anim = Animal(
                name = "patatin",
                date_of_birth = datetime(2029,1,2).date(),
                race = 'bâtard',
                species = 0,
                color = 'grey',
                caution = '100',
                date_of_adoption = datetime.now().date())
            owner.save()
            admin.save()
            anim.save()
            anim.owner = owner
            anim.admin_data = admin
            anim.save()

            return anim
        return already_exists[0]

    def modified_text(self, given_id=None):
        """takes plain text and returns modified text"""
        anim = self._get_false_animal()
        if given_id: 
            anim = Animal.objects.get(id=given_id)
        new_text = self.plain_text
        dict_conversion = converter_data(anim)
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

    def text_mail_template(self, given_id): 
        """this function returns a list of modified_text element"""
        modified_text = self.modified_text(given_id).split('\\n')
        for elem in modified_text: 
            if len(elem) < 1: 
                modified_text.remove(elem)
        return modified_text

    def send_auto_mail(self, send_to, given_id):
        """this function sends an auto mail according to its values and param """
        modified_text = self.text_mail_template(given_id)
        html_mail = get_template('mail/mail_template.html')
        context = {"text" : modified_text}
        html_content = html_mail.render(context)
        try:
            send_mail(
                subject=self.resume, 
                message=None , 
                from_email='blingstand@hotmail.fr', 
                recipient_list=['adrien.clupot@gmail.com'],
                html_message=html_content, fail_silently=False)
            print(f"send_auto_mail > mail send to {send_to}")
            print("//*protection*\\\\ : mail redirigé vers adrien.clupot@gmail.com")
        except Exception as e:
            raise e

