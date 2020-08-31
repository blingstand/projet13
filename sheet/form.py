""" script for the needed form"""

from datetime import date

from django import forms
from django.db.utils import IntegrityError

from .models import *

CHOICES = (
    ("1", "chat"),("2", "chatte"), ("3", "chien"), ("4", "chienne"))
CHOICE_STERIL = (1,"stérile"), (2,"stérilisable"), (3,"sera stérilisable")
CHOICE_SEX = (('H',"Homme"), ('F',"Femme"))
class PersonalErrorMsg(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class DateInput(forms.DateInput):
    input_type = 'date'
class SheetForm(forms.Form):
    """form to add a new sheet """
    caution = forms.CharField(required=True, max_length=30, label='caution', 
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 
            'title' : 'montant de la caution',
            'placeholder' : "montant de la caution"}))
    chip = forms.CharField(required=False,  label='puce',
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : 'num de la puce',
            'placeholder' : "num de la puce"}))
    date_of_adoption = forms.DateField(required=True, label="date d'adoption",
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date d'adoption ",
             "class":"w-10rem", 
             'title':"date d'adoption (jj/mm/aaa)"}))
    date_of_birth = forms.DateField(required=True, label="date de naissance",
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date de naissance ",
             "class":"w-10rem", 
             'title':"date de naissance (jj/mm/aaa)"}))
    date_of_neuter = forms.DateField(required=False, label="date de stérilisation",
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date de stérilisation ",
             "class":"w-10rem", 
             'title':"date de stérilisation (jj/mm/aaa)"}))
    futur_date_of_neuter = forms.DateField(required=False, 
        widget=forms.TextInput(attrs={ 
            'placeholder' : " à partir du :  ",
            "class":"w-10rem", 
            'title':"stérilisable à partir du (jj/mm/aaa)"}))
    file = forms.CharField(required=False, label='dossier',
        widget=forms.TextInput(attrs={'class' : 'input-reduced',  'title' : "num du dossier",
            'placeholder' : "num du dossier"}))
    is_neutered = forms.ChoiceField(required=True, 
        widget=forms.RadioSelect(attrs={"class" : "lst-none pl-0 mb-0"}), 
        choices=(CHOICE_STERIL))
    mail = forms.EmailField(required=True, max_length=30, label='mail',
        widget=forms.TextInput(attrs={'class' : 'text-center', 'title' : 'mail' ,
            'placeholder' : "mail"}))
    mail_reminder = forms.IntegerField(required=True, label='nb mail',
        widget=forms.NumberInput(attrs={ 'class' : 'input-reduced', 'title' : 'nb rappel mail' ,
            'placeholder' : "nb rappel mail",'min':0}))
    name = forms.CharField(required=True, label="Nom de l'animal", max_length=30, 
        widget=forms.TextInput(attrs={ 'title' : "nom de l'animal",
            'placeholder' : "nom de l'animal", "class":"w-10rem"}))
    status = forms.CharField(required=False, max_length=200, 
        widget=forms.Textarea(attrs={ 'title' : "statut de la stérilisation",
            'placeholder' : "statut de la stérilisation", 'cols':30, 'rows':3}))
    owner_name = forms.CharField(required=True, label="prénom", max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "propriétaire" ,
            'placeholder' : "prénom du propriétaire"}))
    owner_surname = forms.CharField(required=True, label="nom", max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "propriétaire" ,
            'placeholder' : "nom du propriétaire"}))
    owner_sex = forms.ChoiceField(label="Sexe", required=True, 
        widget=forms.RadioSelect(attrs={'class' : 'li-oneline '}), choices=CHOICE_SEX)
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
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "téléphone",
            'placeholder' : "téléphone"}))
    tel_reminder = forms.IntegerField(required=True, label='nb appel', 
        widget=forms.NumberInput(attrs={ 'class' : 'input-reduced', 'title' : "nb rappel téléphonique",
            'placeholder' : "nb rappel tel",'min':0, "values":0}))


    def _handle_admin_class(self, dict_values):
        #create and save admin classe
        list_admin = dict_values['admin']
        admin = AdminData(*list_admin)
        queryset = AdminData.objects.filter(chip=admin.chip,file=admin.file, tatoo=admin.tatoo)
        same_in_db = len(AdminData.objects.filter(chip=admin.chip,file=admin.file, tatoo=admin.tatoo)) > 0
        if same_in_db:
            return False, f"Erreur : ce dossier admin existe déjà dans la base, risque de doublon, procédure annulée !"
        admin.save()
        return True, admin

    def _handle_owner_class(self, dict_values):
        #create and save owner classe
        #already exists ? 
        list_owner = dict_values['owner']
        owner_in_db = Owner.objects.filter(owner_name=list_owner[1], owner_surname=list_owner[2])
        owner = Owner(*list_owner)
        if len(owner_in_db) > 0:
            owner.id = owner_in_db[0].id #have to give because auto increment is on for id
            for elem in ('id','owner_name', 'owner_surname','owner_sex',  'phone', 'mail', 'tel_reminder', 'mail_reminder', 'caution'):
                if getattr(owner, elem) != getattr(owner_in_db[0], elem):
                    print('diff')
                    owner.id == None
            print('Cet utilisateur existe déjà je récupère sa fiche.')
            return True, owner

        else:
            print("Création d'un nouvel utilisateur ...")
            try: 
                owner.save()
                print('je retourne :', owner)
                return True, owner
            except IntegrityError as ie: 
                if "tel" in str(ie):
                    return False , "Ce téléphone existe déjà dans la base ! Procédure annulée ..."
                elif "mail" in str(ie):
                    return False, "Ce mail existe déjà dans la base ! Procédure annulée ... "
            except Exception as e: 
                print(e)
            
    def _handle_animal_class(self, dict_values):
        #create and save animal classe
        #animal already exists
        list_ani = dict_values['animal']
        animal = Animal(*list_ani)  
        same_in_base = Animal.objects.filter(name=animal.name)
        if len(same_in_base) > 0:
            print(type(same_in_base))
            print(f'comparaison : {same_in_base == animal}')
            print('*'*20)
            if same_in_base == animal:
                return False, 'Cet animal existe déjà dans la base de données.'
        animal.save()   
        return True, animal

    def from_form(self):
        """ returns dictionary of values to fill rows in tables """
        animal = ('name', 'date_of_birth', 'race', 'species', 'color', 'date_of_adoption', 'observation')
        admin = ('file', 'chip', 'tatoo', 'is_neutered', 'date_of_neuter', 'futur_date_of_neuter', 'status')
        owner = ('owner_name', 'owner_surname','owner_sex',  'phone', 'mail', 'tel_reminder', 'mail_reminder', 'caution')
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

    def save_data(self, dict_values):
        """ save the data in database and return """

        #transaction : one fails all fail
        succes1, output = self._handle_admin_class(dict_values)
        if succes1:
            admin = output
            print('- données pour admin ok ')
        else:
            error_msg = output
            return error_msg
        succes2, output = self._handle_owner_class(dict_values)
        if succes2: 
            owner = output
            print('- données pour owner ok ')
        else:
            admin.delete()
            print("deleted")
            error_msg = output
            return error_msg
        succes3, output = self._handle_animal_class(dict_values)
        if succes3:
            animal = output
            animal.admin_data = admin
            animal.owner = owner
            print('vérification : ad/ow ||',animal.admin_data, animal.owner )
            animal.save()
            print('- données pour animal ok ')
            return 1
        else:
            animal.delete()
            owner.delete()
            print('\t- erreur pour owner, effacement données admin et owner.')
            error_msg = output
            return error_msg 
        


    """
        name_col = ('name','date_of_birth','race','species','color','date_of_adoption', 'picture')
    """