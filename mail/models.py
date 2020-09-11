from django.db import models
import datetime
import locale
locale.setlocale(locale.LC_TIME,'')
# Create your models here.
class Mail(models.Model):
    mail_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    resume = models.CharField(blank=True, max_length=120)
    full_text = models.TextField(blank=True)
    auto_send = models.BooleanField(blank=True,default=False)
    send_after_creation = models.BooleanField(blank=True,default=None)
    send_after_modif = models.BooleanField(blank=True,default=None)
    send_when_x_month = models.IntegerField(blank=True,default=None, null=True)
    send_at_this_date = models.DateField(null=True, blank=True, default=None)

    def __str__(self):
        if self.mail_id is not None: 
            return f'mail{self.mail_id} (titre: {self.title})'
        return f'mail(titre: {self.title})'

    def get_condition(self): 
        #this function returns a condition(str) if auto_send = true, else returns None 
        condition = {
            self.send_after_creation : (bool, 'à la création de la fiche'),
            self.send_after_modif : (bool, 'à la modification de la fiche'),
            self.send_when_x_month : (int, f"pour les {self.send_when_x_month} mois de l'animal"),
            self.send_at_this_date : (datetime, f'à la date du {self.send_at_this_date}')}

        if self.auto_send == False: 
            return None
        for key in condition:
            if isinstance(key, condition[key][0]):
                if key == False:
                    continue
                return condition[key][1]




