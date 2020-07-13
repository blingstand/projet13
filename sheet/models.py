from django.db import models
from django.utils import timezone


class Animal(models.Model):
    animal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="Nom")
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    race = models.CharField(max_length=50)
    species = models.CharField(max_length=7, default='chat', verbose_name="chat/chatte/chien/chienne")
    color = models.CharField(max_length=30, blank=True, verbose_name="Couleur")
    date_of_adoption = models.DateField(verbose_name="Date d'adoption",)
    picture = models.FileField(blank=True, null=True, upload_to="animals/", default = 'animals/no-img.j')
    admin_data = models.OneToOneField('AdminData', on_delete=models.CASCADE, 
        verbose_name="Suivi administratif", null=True, blank=True, unique=True)
    owner = models.ForeignKey('Owner', on_delete=models.PROTECT, 
        verbose_name="Propriétaire", null=True, blank=True)
    def __str__(self):
        return self.name

class AdminData(models.Model):
    admin_data_id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de dossier")
    chip = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de puce")
    tatoo = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de tatouage")
    is_neutered = models.BooleanField(default=False, verbose_name="Stérilisé")
    date_of_neuter = models.DateField(null=True, blank=True, verbose_name="Date de stérilisation")
    status = models.TextField(null=True, blank=True, max_length=200, 
        verbose_name="Explication concernant la stérilisation")
    def __str__(self):
        return f"dossier {self.admin_data_id}"

class Owner(models.Model):
    owner = models.CharField(unique=True, max_length=50, null=True, blank=False, verbose_name="Idt du proprio")
    phone = models.CharField(unique=True, max_length=30, verbose_name="Téléphone")
    mail = models.EmailField(unique=True, verbose_name="Mail")
    tel_reminder = models.SmallIntegerField(default=0, verbose_name="Nombre d'appel passés")
    mail_reminder = models.SmallIntegerField(default=0, verbose_name="Nombre de mail envoyés")
    caution = models.CharField(max_length=30, null=True, default="null",
        verbose_name="Caution + support (ex : 200e en chèque)")
    contact_id = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name="Gestion des contacts", 
        null=True, blank=True)
    def __str__(self):
        return self.owner

class Contact(models.Model):

    contact_date = models.DateField(default=timezone.now, verbose_name="Date du contact")
    resume = models.CharField(blank=True, max_length=90)
    full_text = models.TextField(blank=True)
    is_mail = models.BooleanField(default=True)
    def __str__(self):
        return f"suivi contact {self.contact_id}"
    