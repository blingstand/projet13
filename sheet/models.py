""" models for sheet app """
#from python
from datetime import datetime, timedelta
#from django
from django.db import models
from django.db.models import Q
from django.utils import timezone
class Animal(models.Model):
    """class for animal """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="Nom") #2 animaux peuvent avoir le même nom
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    race = models.CharField(max_length=50)
    species = models.CharField(max_length=1, verbose_name="chat/chatte/chien/chienne")
    color = models.CharField(max_length=30, blank=True, verbose_name="Couleur")
    date_of_adoption = models.DateField(verbose_name="Date d'adoption",)
    observation = models.CharField(max_length=50, blank=True)
    caution = models.CharField(max_length=5, verbose_name="Montant de la caution(sans €)")
    nature_caution = models.CharField(max_length=20, default="chèque", \
        verbose_name="Nature de la caution(sans €)")
    picture = models.FileField(blank=True, null=True, upload_to="animals/",\
     default = 'animals/no-img.j')
    admin_data = models.OneToOneField('AdminData', on_delete=models.CASCADE,
        verbose_name="Suivi administratif", null=True, blank=True, unique=True)
    owner = models.ForeignKey('Owner', on_delete=models.PROTECT,
        verbose_name="Propriétaire", null=True, blank=True)
    def __str__(self):
        """ this function modifies the str of animal class object"""
        try :
            if self.admin_data.file is not None:
                return f'{self.name} (dossier : {self.admin_data.file})'
            else:
                return self.name
        except:
            return self.name
    @property
    def str_species(self):
        """ this function returns human readable species values """
        species = ("0", "chat"),("1", "chatte"), ("2", "chien"), ("3", "chienne")
        species_name = lambda x : species[int(x)][1]
        return species_name(self.species)
class AdminData(models.Model):
    """ class for admin_datas """
    id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=15, null=True, blank=True, \
        verbose_name="Numéro de dossier")
    chip = models.CharField(max_length=15, null=True, blank=True, \
        verbose_name="Numéro de puce")
    tatoo = models.CharField(max_length=15, null=True, blank=True, \
        verbose_name="Numéro de tatouage")
    is_neutered = models.CharField(max_length=1, default=0, \
        verbose_name="statut stérilisation (stérile, stérilisable, à stériliser)")
    date_of_neuter = models.DateField(null=True, blank=True, \
        verbose_name="A été stérilisé(e) le")
    futur_date_of_neuter = models.DateField(null=True, blank=True, \
        verbose_name="Sera stérilisable le")
    status = models.TextField(null=True, blank=True, max_length=200,
        verbose_name="Explication concernant la stérilisation")
    def __str__(self):
        """ this function modifies the str of admin class object """
        if self.file:
            return f"dossier {self.file}"
        elif self.chip:
            return f"puce {self.chip}"
        else:
            return f"tatoo {self.tatoo}"
    @property
    def neuter_status(self):
        """ this function displays a human readable neuter value """
        ststatus = (0,"stérile"), (2,"stérilisable"), (3,f"pas encore stérilisable")
        if self.futur_date_of_neuter is not None:
            ststatus = (0,"stérile"), (2,"stérilisable"), \
            (3,f"stérilisable dès le {self.futur_date_of_neuter.strftime('%d/%m/%Y')}")
        neuter_status = lambda x : ststatus[int(x)][1]
        return neuter_status(self.is_neutered)
class Owner(models.Model):
    """ class for owner sheet """
    owner_name = models.CharField(max_length=50, null=True, \
    verbose_name="Prénom propriétaire")#1 owner can have same name
    owner_surname = models.CharField(max_length=50, null=True, \
    verbose_name="Nom propriétaire")#1 owner can have same surname
    owner_sex = models.CharField(max_length=1, default=0, null=True, \
        verbose_name="Sexe propriétaire\n (0 = H / 1 = F)")
    phone = models.CharField(unique=True, max_length=30, verbose_name="Téléphone")
    mail = models.EmailField(unique=True, verbose_name="Mail")
    tel_reminder = models.CharField(max_length=3, default=0, verbose_name="Nombre d'appel passés")
    mail_reminder = models.CharField(max_length=3, default=0, verbose_name="Nombre de mail envoyés")
    def __str__(self):
        """ this function modifies str owner class object """
        if self.owner_sex == "0":
            return f'M. {self.owner_surname.upper()} {self.owner_name}'
        else:
            return f'Mme {self.owner_surname.upper()} {self.owner_name}'
    @property
    def apostrophe(self):
        """ this function displays human readable owner_sex"""
        if self.owner_sex == "0":
            return 'Monsieur'
        else:
            return 'Madame'

    @property
    def small_apostrophe(self):
        """ this function displays human readable owner_sex"""
        if self.owner_sex == "0":
            return 'M.'
        else:
            return 'Mme'
    
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
    @property
    def last_contact(self):
        """ this function returns most recent contact from owner or None """
        contacts = Contact.objects.filter(Q(owner=self, nature=3) | Q(owner=self, nature=4))
        contacts = contacts.order_by('-contact_date')
        if len(contacts) > 0:
            return contacts[0]
        return None
    @property
    def to_contact(self):
        """ this function returns True if last contact is bigger than 1 week """
        contacts = Contact.objects.filter(owner=self).order_by('contact_date')
        # print("list contact pour vérif : ")
        # print(self, [contact.contact_date for contact in contacts])
        if len(contacts) == 0:
            pass
        else:
            last_contact = contacts[0].contact_date
            if len(contacts) > 1:
                last_contact = contacts[-1].contact_date
            now = datetime.now().date()
            more_than_a_week = now >= (last_contact + timedelta(weeks=1))
            print("is more_than_a_week >", now, " >= ", last_contact + timedelta(weeks=1))
            print("is more_than_a_week >", type(now), " >= ", type(last_contact + timedelta(weeks=1)))
            print(more_than_a_week)
            if more_than_a_week:
                return True
            return False
    @property
    def refresh_sum_mail(self):
        """ this function refresh the value of mail_reminder according to contact nature in db """
        nature1 = Contact.objects.filter(nature=1, owner=self)
        nature3 = Contact.objects.filter(nature=3, owner=self)
        nature5 = Contact.objects.filter(nature=5, owner=self)
        sum_mail = len(nature1) + len(nature3) + len(nature5)
        self.mail_reminder = sum_mail
        self.save()
        return sum_mail
    @property
    def refresh_sum_tel(self):
        """ this function refresh the value of tel_reminder according to contact nature in db """
        nature2 = Contact.objects.filter(nature=2, owner=self)
        nature4 = Contact.objects.filter(nature=4, owner=self)
        sum_tel = len(nature2) + len(nature4)
        self.tel_reminder = sum_tel
        self.save()
        return sum_tel
class Contact(models.Model):
    """ class for contact sheet """
    contact_date = models.DateField(default=timezone.now, verbose_name="Date du contact")
    resume = models.CharField(default="A compléter ...", max_length=90)
    full_text = models.TextField(default="A compléter ...")
    nature = models.CharField(default="à compléter", max_length=1)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Gestion des contacts",
        null=True, blank=True)
    def __str__(self):
        """ this function modifes str for contact class objects """
        return f"Contact n°{self.id} du {self.contact_date} (type: {self.nature}) "
    @property
    def str_nature(self):
        """this function returns a readable nature data"""
        conversion = [
        {'nature' : "0", "str_nature": "sélectionnez un type"},
        {'nature' : "1", "str_nature": "mail spa"},
        {'nature' : "2", "str_nature": "tel spa"},
        {'nature' : "3", "str_nature": "mail propriétaire"},
        {'nature' : "4", "str_nature": "tel propriétaire"},
        {'nature' : "5", "str_nature": "mail automatique"},
        ]
        for dic in conversion:
            if dic["nature"] == self.nature:
                return dic['str_nature']
    @property
    def reduced_text(self):
        """ this function limits text to 150 characters"""
        text = self.escaped_charac_text[0:100] + " ..."
        return text
    @property
    def escaped_charac_text(self):
        """ this function escapes \n character """
        elem = '\\n\\n'
        text = self.full_text.replace(elem, "\n")
        return text
