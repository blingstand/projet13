from django.db import models

# Create your models here.
class Mail(models.Model):
    mail_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    resume = models.CharField(blank=True, max_length=120)
    full_text = models.TextField(blank=True)

    def __str__(self):
        return f'mail : {self.title}'