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
    
    def _get_false_animal(self):
        """this function returns a fictif animal in order to display an overview"""
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
        animal = Animal(
            name = "patatin",
            date_of_birth = datetime(2029,1,2).date(),
            race = 'bâtard',
            species = 0,
            color = 'grey',
            caution = '100',
            date_of_adoption = datetime.now().date())
        anim.owner = owner
        anim.admin_data = admin
        return anim

    def modified_text(self, given_id=None):
        """takes plain text and returns modified text"""
        print("-- modified_text pour ", given_id)
        anim = Animal.objects.all()[0]
        if given_id: 
            anim = Animal.objects.get(id=given_id)
            print("given_id reçu >>", anim)
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


    def send_auto_mail(self, send_to, given_id):
        """this function sends an auto mail according to its values and param """
        text = self.modified_text(given_id)
        print("-- send_auto_mail, pour cet id : ")
        print(text)
        try:
            send_mail(
                self.resume, text , 'blingstand@hotmail.fr', 
                ['adrien.clupot@gmail.com'], fail_silently=False)
            print(f"send_auto_mail > mail send to {send_to}")
        except Exception as e:
            raise e

