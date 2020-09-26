from django.db import models
from django.utils import timezone


class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="Nom") #2 animaux peuvent avoir le même nom  
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    race = models.CharField(max_length=50)
    species = models.CharField(max_length=1, verbose_name="chat/chatte/chien/chienne")
    color = models.CharField(max_length=30, blank=True, verbose_name="Couleur")
    date_of_adoption = models.DateField(verbose_name="Date d'adoption",)
    observation = models.CharField(max_length=50, blank=True)
    caution = models.PositiveSmallIntegerField(default=0, verbose_name="Montant de la caution(sans €)")
    nature_caution = models.CharField(max_length=20, default="chèque", verbose_name="Nature de la caution(sans €)")
    picture = models.FileField(blank=True, null=True, upload_to="animals/", default = 'animals/no-img.j')
    admin_data = models.OneToOneField('AdminData', on_delete=models.CASCADE, 
        verbose_name="Suivi administratif", null=True, blank=True, unique=True)
    owner = models.ForeignKey('Owner', on_delete=models.PROTECT, 
        verbose_name="Propriétaire", null=True, blank=True)
    def __str__(self):
        try :
            if self.admin_data.file is not None: 
                return f'{self.name} (dossier : {self.admin_data.file})'
            else:
                return self.name
        except:
            return self.name
    @property    
    def species_name(self): 
        species = ("0", "chat"),("1", "chatte"), ("2", "chien"), ("3", "chienne")
        species_name = lambda x : species[int(x)][1]
        return species_name(self.species)



class AdminData(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de dossier")
    chip = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de puce")
    tatoo = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de tatouage")
    is_neutered = models.CharField(max_length=1, default=0, verbose_name="statut stérilisation (stérile, stérilisable, à stériliser)")
    date_of_neuter = models.DateField(null=True, blank=True, verbose_name="A été stérilisé(e) le")
    futur_date_of_neuter = models.DateField(null=True, blank=True, verbose_name="Sera stérilisable le")
    status = models.TextField(null=True, blank=True, max_length=200, 
        verbose_name="Explication concernant la stérilisation")
    def __str__(self):
        if self.file:
            return f"dossier {self.file}"
        elif self.chip:
            return f"puce {self.chip}"
        else:
            return f"tatoo {self.tatoo}"
    @property
    def neuter_status(self):
        ststatus = (0,"stérile"), (2,"stérilisable"), (3,"sera stérilisable")
        neuter_status = lambda x : ststatus[int(x)][1]
        return neuter_status(self.is_neutered)
    

class Owner(models.Model):
    owner_name = models.CharField(max_length=50, null=True, verbose_name="Prénom propriétaire")#1 owner can have same name
    owner_surname = models.CharField(max_length=50, null=True, verbose_name="Nom propriétaire")#1 owner can have same surname
    owner_sex = models.CharField(max_length=1, default=0, null=True, verbose_name="Sexe propriétaire\n (0 = H / 1 = F)")
    phone = models.CharField(unique=True, max_length=30, verbose_name="Téléphone")
    mail = models.EmailField(unique=True, verbose_name="Mail")
    tel_reminder = models.CharField(max_length=3, default=0, verbose_name="Nombre d'appel passés")
    mail_reminder = models.CharField(max_length=3, default=0, verbose_name="Nombre de mail envoyés")

    def __str__(self):
        if self.owner_sex == "0":
            return f'Monsieur {self.owner_surname.upper()} {self.owner_name}'
        else:
            return f'Madame {self.owner_surname.upper()} {self.owner_name}'

    def number_animal(self): 
        """ this function returns how many animals belong to this owner """
        animal = Animal.objects.filter(owner=self)
        return len(animal)
    @property
    def sum_caution(self):
        """ this function calculate the sum of all caution of animal that belongs to this owner """
        all_cautions = [animal.caution for animal in Animal.objects.filter(owner=self)]
        total = 0
        for caution in all_cautions:
            total += int(caution) 
        return total
        
class Contact(models.Model):

    contact_date = models.DateField(default=timezone.now, verbose_name="Date du contact")
    resume = models.CharField(default="A compléter ...", max_length=90)
    full_text = models.TextField(default="A compléter ...")
    nature = models.CharField(default="à compléter", max_length=20) 
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Gestion des contacts", 
        null=True, blank=True)
    def __str__(self):
        return f"Contact n°{self.id} du {self.contact_date} (type: {self.nature}) "
    