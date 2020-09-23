from django.db import models
from django.utils import timezone


class Animal(models.Model):
    animal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="Nom") #2 animaux peuvent avoir le même nom  
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    race = models.CharField(max_length=50)
    species = models.CharField(max_length=1, verbose_name="chat/chatte/chien/chienne")
    color = models.CharField(max_length=30, blank=True, verbose_name="Couleur")
    date_of_adoption = models.DateField(verbose_name="Date d'adoption",)
    observation = models.CharField(max_length=50, blank=True)
    picture = models.FileField(blank=True, null=True, upload_to="animals/", default = 'animals/no-img.j')
    admin_data = models.OneToOneField('AdminData', on_delete=models.CASCADE, 
        verbose_name="Suivi administratif", null=True, blank=True, unique=True)
    owner = models.ForeignKey('Owner', on_delete=models.PROTECT, 
        verbose_name="Propriétaire", null=True, blank=True)
    def __str__(self):
        try :
            if self.admin_data.file is not None: 
                return f'{self.name} (dossier : {self.admin_data.file})'
            if self.admin_data.chip is not None: 
                return f'{self.name} (puce : {self.admin_data.chip})'
            if self.admin_data.tatoo is not None: 
                return f'{self.name} (tatouage : {self.admin_data.tatoo})'
            else:
                return self.name
        except:
            return self.name


class AdminData(models.Model):
    admin_data_id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de dossier")
    chip = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de puce")
    tatoo = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de tatouage")
    is_neutered = models.CharField(max_length=1, default=0, verbose_name="statut stérilisation (stérile, stérilisable, à stériliser)")
    date_of_neuter = models.DateField(null=True, blank=True, verbose_name="A été stérilisé(e) le")
    futur_date_of_neuter = models.DateField(null=True, blank=True, verbose_name="Sera stérilisé(e) le")
    status = models.TextField(null=True, blank=True, max_length=200, 
        verbose_name="Explication concernant la stérilisation")
    def __str__(self):
        if self.file:
            return f"dossier {self.file}"
        elif self.chip:
            return f"puce {self.chip}"
        else:
            return f"tatoo {self.tatoo}"

class Owner(models.Model):
    owner_name = models.CharField(max_length=50, null=True, verbose_name="Prénom propriétaire")#1 owner can have same name
    owner_surname = models.CharField(max_length=50, null=True, verbose_name="Nom propriétaire")#1 owner can have same surname
    owner_sex = models.CharField(max_length=1, default=0, null=True, verbose_name="Sexe propriétaire\n (0 = H / 1 = F)")
    phone = models.CharField(unique=True, max_length=30, verbose_name="Téléphone")
    mail = models.EmailField(unique=True, verbose_name="Mail")
    tel_reminder = models.CharField(max_length=3, default=0, verbose_name="Nombre d'appel passés")
    mail_reminder = models.CharField(max_length=3, default=0, verbose_name="Nombre de mail envoyés")
    caution = models.CharField(max_length=30, null=True, default="null",
        verbose_name="Caution + support (ex : 200e en chèque)")
    need_contact = models.BooleanField(default=True, verbose_name="besoin d'être contacté(e)")
    contact= models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name="Gestion des contacts", 
        null=True, blank=True)
    def __str__(self):
        if self.owner_sex == "0":
            return f'Monsieur {self.owner_surname.upper()} {self.owner_name}'
        else:
            return f'Madame {self.owner_surname.upper()} {self.owner_name}'

    def number_animal(self): 
        """ this function returns how many animals belong to this owner """
        animal = Animal.objects.filter(owner=self)
        return len(animal)
        
class Contact(models.Model):

    contact_date = models.DateField(default=timezone.now, verbose_name="Date du contact")
    resume = models.CharField(blank=True, max_length=90)
    full_text = models.TextField(blank=True)
    is_mail = models.BooleanField(default=True)
    def __str__(self):
        return f"suivi contact {self.contact_id}"
    