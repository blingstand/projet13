from django.db import models
from django.utils import timezone


class Animal(models.Model):
    animal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="Nom")
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    race = models.CharField(max_length=50)
    is_cat = models.BooleanField(default=True, verbose_name="Espèce : Cocher si c'est un chat")
    color = models.CharField(max_length=30, verbose_name="Couleur")
    is_male = models.BooleanField(default=True, verbose_name="Sexe : Cocher si c'est un mâle") 
    date_of_adoption = models.DateField(default=timezone.now, verbose_name="Date d'adoption", )
    admin_data_id = models.OneToOneField('AdminData', on_delete=models.CASCADE, verbose_name="Suivi administratif")
    owner_id = models.ForeignKey('Owner', on_delete=models.PROTECT, verbose_name="Propriétaire")
    def __str__(self):
        return self.name

class AdminData(models.Model):
    admin_data_id = models.AutoField(primary_key=True)
    file = models.IntegerField(unique=True, null=True, blank=True, verbose_name="Numéro de dossier")
    chip = models.IntegerField(unique=True, null=True, blank=True, verbose_name="Numéro de puce")
    tatoo = models.IntegerField(unique=True, null=True, blank=True, verbose_name="Numéro de tatouage")
    is_neutered = models.BooleanField(default=False, verbose_name="Stérilisé")
    can_be_neutered = models.BooleanField(default=False, verbose_name="Doit être stérilisé")
    def __str__(self):
        return f"dossier {self.admin_data_id}"

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="Nom")
    surname = models.CharField(max_length=30, verbose_name="Prénom")
    telephone = models.IntegerField(unique=True, verbose_name="Téléphone")
    mail = models.EmailField(unique=True, verbose_name="Mail")
    nb_mail_send = models.SmallIntegerField(default=0, verbose_name="Nombre de mail envoyés")
    nb_call = models.SmallIntegerField(default=0, verbose_name="Nombre d'appel passés")
    contact_id = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name="Gestion des contacts", null=True, blank=True)
    def __str__(self):
        return self.name

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_date = models.DateField(default=timezone.now, verbose_name="Date du contact")
    resume = models.CharField(blank=True, max_length=90)
    full_text = models.TextField(blank=True)
    is_mail = models.BooleanField(default=True)
    def __str__(self):
        return f"suivi contact {self.contact_id}"
    