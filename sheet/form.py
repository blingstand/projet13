""" script for the needed form"""

from datetime import datetime, date

from django import forms
from django.forms import ModelForm
from django.db.utils import IntegrityError

from .models import *
from .utils import UtilsSheet

ut = UtilsSheet()

CHOICES = (
    ("0", "chat"),("1", "chatte"), ("2", "chien"), ("3", "chienne"))
CHOICE_STERIL = ("0","stérile"), ("1","stérilisable"), ("2","sera stérilisable")
CHOICE_SEX = (("0","Homme"), ("1","Femme"))
CHOICES_NATURE = (("0", "mail automatique"),("1", "mail spa"), ("2", "tel spa"), \
    ("3", "mail propriétaire"), ("4", "tel propriétaire"))
CHOICES_CAUTION = ("0","chèque"), ("1","virement"), ("2","espèces")
class PersonalErrorMsg(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class DateInput(forms.DateInput):
    input_type = 'date'
class SheetForm(forms.Form):
    """form to add a new sheet """   
    caution = forms.IntegerField(required=True, label='caution', initial='100',
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 
            'title' : 'montant de la caution',
            'placeholder' : "montant (sans €)"}))
    chip = forms.CharField(required=False,  label='puce',
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : 'num de la puce',
            'placeholder' : "num de la puce"}))
    date_of_adoption = forms.DateField(required=True, label="date d'adoption",
        widget=forms.DateInput(attrs={ 
            'placeholder' : "jj/mm/aaaa ",
            'type' : 'date',
            "class":"w-10rem", 
            'title':"date d'adoption (jj/mm/aaa)"}))
    date_of_birth = forms.DateField(required=True, label="date de naissance",
        widget=forms.DateInput(attrs={ 
            'placeholder' : "jj/mm/aaaa",
            'type' : 'date',
            "class":"w-10rem", 
            'title':"date de naissance (jj/mm/aaa)"}))
    date_of_neuter = forms.DateField(required=False, label="date de stérilisation",
        widget=forms.DateInput(attrs={ 
            'placeholder' : "jj/mm/aaaa",
            'type' : 'date',
             "class":"w-10rem", 
             'title':"date de stérilisation (jj/mm/aaa)"}))
    futur_date_of_neuter = forms.DateField(required=False, label="dès le : ",
        widget=forms.DateInput(attrs={ 
            'placeholder' : "jj/mm/aaaa",
            'type' : 'date',
            "class":"w-10rem", 
            'title':"stérilisable à partir du (jj/mm/aaa)"}))
    file = forms.CharField(required=False, label='dossier',
        widget=forms.TextInput(attrs={'class' : 'input-reduced',  'title' : "num du dossier",
            'placeholder' : "num du dossier"}))
    is_neutered = forms.ChoiceField(required=True, 
        widget=forms.RadioSelect(attrs={"class" : "lst-none pl-0 mb-0"}), 
        choices=(CHOICE_STERIL))
    mail = forms.EmailField(required=True, max_length=30, label='mail',
        widget=forms.EmailInput(attrs={'class' : 'text-center', 'title' : 'mail' ,
            'placeholder' : "mail", 'name' : 'mail'}))
    mail_reminder = forms.IntegerField(required=True, label='nb mail',initial='0', 
        widget=forms.NumberInput(attrs={ 'class' : 'input-very-reduced', 'title' : 'nb rappel mail' ,
            'placeholder' : "nb rappel mail",'min':0}))
    name = forms.CharField(required=True, label="Nom de l'animal", max_length=30, 
        widget=forms.TextInput(attrs={ 'title' : "nom de l'animal",
            'placeholder' : "nom de l'animal", "class":"w-10rem"}))
    nature_caution = forms.CharField(required=True, label="nature : ", max_length=20, 
        widget=forms.Select(attrs={ 'title' : "Nature de la caution",
            "class":"w-10rem"}, choices=CHOICES_CAUTION))
    status = forms.CharField(required=False, max_length=200, 
        widget=forms.Textarea(attrs={ 'title' : "statut de la stérilisation",
            'placeholder' : "statut de la stérilisation", 'cols':30, 'rows':3}))
    owner_name = forms.CharField(required=True, label="prénom", max_length=30, 
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "propriétaire" ,
            'placeholder' : "prénom proprio", 'name':"Prénom"}))
    owner_surname = forms.CharField(required=True, label="nom", max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "propriétaire" ,
            'placeholder' : "nom proprio", 'name':"Nom"}))
    owner_sex = forms.ChoiceField(label="Sexe", required=True, 
        widget=forms.RadioSelect(attrs={'class' : 'li-oneline very-center', 'name':"Sexe"}), choices=CHOICE_SEX)
    observation = forms.CharField(required=False, max_length=50, label='observation(s)',
        widget=forms.TextInput(attrs={ 'title' : "observation(s)",
            'placeholder' : "observation(s)"}))
    color = forms.CharField(required=True, max_length=30, label='couleur',
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "couleur(s) de l'animal",
            'placeholder' : "couleur(s) de l'animal"}))
    race = forms.CharField(required=True, label="race", max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "race de l'animal" ,
            'placeholder' : "race de l'animal"}))
    species = forms.ChoiceField(widget=forms.RadioSelect(attrs={"class" : "lst-none pl-0"}), choices=CHOICES)
    tatoo = forms.CharField(required=False, label='tatouage', 
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "num de tatouage" ,
            'placeholder' : "num de tatouage"}))
    phone = forms.CharField(required=True, max_length=15, label='tel', 
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "téléphone",'name':"Téléphone",
            'placeholder' : "téléphone"}))
    tel_reminder = forms.IntegerField(required=True, label='nb appel', initial='0', 
        widget=forms.NumberInput(attrs={ 'class' : 'input-very-reduced', 'title' : "nb rappel téléphonique",
            'placeholder' : "nb rappel tel",'min':0, "values":0}))

    def _handle_admin_class(self, dict_values):
        #create and save admin classe
        list_admin = dict_values['admin']
        admin = AdminData(*list_admin)
        queryset = AdminData.objects.filter(chip=admin.chip,file=admin.file, tatoo=admin.tatoo)
        same_in_db = len(AdminData.objects.filter(chip=admin.chip,file=admin.file, tatoo=admin.tatoo)) > 0
        if same_in_db:
            return False, f"Erreur : ce dossier admin existe déjà dans la base, risque de doublon, procédure annulée !"
        return True, admin

    def _handle_owner_class(self, dict_values):
        #already exists or namesake ? 
        list_owner = dict_values['owner']
        query = Owner.objects.filter(owner_name=list_owner[1], owner_surname=list_owner[2], phone=list_owner[4], mail=list_owner[5])
        already_exists = (len(query) != 0)
        print("_handle_owner_class, already_exists : ", already_exists)
        if already_exists:
            # print('Cet utilisateur existe déjà je récupère sa fiche.')
            print('je retourne : True, ', query[0])
            return True, query[0]
        else:
            # print("Création d'un nouvel utilisateur ...")
            try: 
                owner = Owner(*list_owner)
                owner.save() #this creates id
                return True, owner
            except IntegrityError as ie: 
                print("ici")
                if "phone" in str(ie):
                    return False , "Ce téléphone existe déjà dans la base ! Procédure annulée ..."
                elif "mail" in str(ie):
                    return False, "Ce mail existe déjà dans la base ! Procédure annulée ... "
            except Exception as e: 
                    return False, f"Procédure annulée > Voici le problème({e})"
            
    def _handle_animal_class(self, dict_values):
        #create and save animal classe
        #animal already exists
        list_ani = dict_values['animal']
        animal = Animal(*list_ani)  
        same_in_base = Animal.objects.filter(name=animal.name, date_of_birth=animal.date_of_birth)
        if len(same_in_base) > 0:
            return False, 'Cet animal existe déjà dans la base de données.'
        animal.species = int(animal.species)
        animal.save()   
        return True, animal

    def from_form(self, ):
        """ returns dictionary of values to fill rows in tables """
        animal = ('name', 'date_of_birth', 'race', 'species', 'color', 'date_of_adoption', 'observation', 'caution', 'nature_caution')
        admin = ('file', 'chip', 'tatoo', 'is_neutered', 'date_of_neuter', 'futur_date_of_neuter', 'status')
        owner = ('owner_name', 'owner_surname','owner_sex',  'phone', 'mail', 'tel_reminder', 'mail_reminder')
        dict_values=self.cleaned_data

        # first element have to stay None because it is for auto-id
        animal = [None] + [dict_values[elem] for elem in animal]
        owner = [None]  + [dict_values[elem] for elem in owner]
        admin = [None]  + [dict_values[elem] for elem in admin]

        dict_values={
            'animal':animal,
            'admin':admin,
            'owner':owner,
            }
        return dict_values
    
    def is_owner_unique(self, owner):
        """this function checks whether owner is unique """
        animals = Animal.objects.filter(owner=owner)   
        is_unique = len(animals) < 1
        return is_unique

    def create_first_contact(self, owner, animal):
        """when a sheet is created > app sends an auto_mail, this function 
        keeps a trace in contact"""
        try:    
            data = {
                "contact_date": datetime.now().date(),
                "nature": "5", 
                "resume": "félicitation + rappel loi",
                "full_text": f"félicitation adoption de {animal.name}({animal.str_species}) + rappel loi sur stérilisation"
            }
            owner.mail_reminder = str(int(owner.mail_reminder) + 1)
            success, output = ut.create_contact(owner, data)
            return success, output
        except Exception as e:
            raise e
            return False, f"problème dans create_first_contact : {e}"

    def save_new_datas(self, dict_values):
        """ save the data in database and return """

        #transaction : one fails all fail
        try : 
            success1, output = self._handle_admin_class(dict_values)
            if not success1:
                error_msg = output
                return error_msg, None
            admin = output
            admin.save()
            # print('- données pour admin ok ')
        except Exception as e:
            print("***")
            print("ERROR : ", e)
            print("***")
            error_msg = output
            return error_msg, None
        try:
            success2, output = self._handle_owner_class(dict_values)
            if success2: 
                print(f"output : {output}")
                owner = output
                owner.save()
                # print('- données pour owner ok ')
            else:
                admin.delete()
                error_msg = output
                return error_msg, None
            pass
        except Exception as e:
            admin.delete()
            return "erreur pour animal, effacement données admin", None
        try:
            success3, output = self._handle_animal_class(dict_values)
            if success3:
                print(f"output : {output}")
                animal = output
                animal.admin_data = admin
                animal.owner = owner
                animal.save()
                # print('- données pour animal ok ')
            else:
                admin.delete()
                response = self.is_owner_unique(owner)
                if response:
                    owner.delete()
                    print('\t- erreur pour animal, effacement données animal, admin et owner (unique).')
                else:
                    print('\t- erreur pour owner, effacement données animal et admin, owner (pas unique).')
                error_msg = output
                return error_msg, None 
        except Exception as e:
            raise e
        success4, output = self.create_first_contact(owner, animal)
        print(f"création 1er contact")
        if success4: 
            return  1, animal
        else: 
            admin.delete()
            response = self.is_owner_unique(owner)
            if response:
                owner.delete()
                print('\t- erreur pour animal, effacement données animal, admin et owner (unique).')
            else:
                print('\t- erreur pour owner, effacement données animal et admin, owner (pas unique).')
            error_msg = output
            return error_msg, None 


        
class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ['contact_date', 'resume', 'full_text', 'nature']
        widgets = {
            'nature': forms.Select(choices=CHOICES_NATURE),
        }
