from django.db import models

# Create your models here.
class Mail(models.Model):
    mail_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    resume = models.CharField(blank=True, max_length=120)
    full_text = models.TextField(blank=True)
    send_after_creation = models.BooleanField(blank=True,default=False)
    send_after_modif = models.BooleanField(blank=True,default=False)
    send_when_x_month = models.IntegerField(blank=True,default=None, null=True)
    send_at_this_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'mail{self.mail_id} (titre: {self.title})'