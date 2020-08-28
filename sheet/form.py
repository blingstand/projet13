""" script for the needed form"""

from datetime import date

from django import forms
from django.db.utils import IntegrityError

from .models import *

CHOICES = (
    ("1", "chat"),("2", "chatte"), ("3", "chien"), ("4", "chienne"))
CHOICE_STERIL = (1,"stérile"), (2,"stérilisable"), (3,"non stérilisable")

class PersonalErrorMsg(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class DateInput(forms.DateInput):
    input_type = 'date'
class SheetForm(forms.Form):
    """form to add a new sheet """
    caution = forms.CharField(required=True, max_length=30, 
        widget=forms.TextInput(attrs={ 
            'title' : 'montant de la caution',
            'placeholder' : "montant de la caution"}))
    chip = forms.CharField(required=False,  
        widget=forms.TextInput(attrs={ 'title' : 'num de la puce',
            'placeholder' : "num de la puce"}))
    date_of_adoption = forms.DateField(required=True, 
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date d'adoption ",
             "class":"w-10rem", 
             'title':"date d'adoption (jj/mm/aaa)"}))
    date_of_birth = forms.DateField(required=True, 
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date de naissance ",
             "class":"w-10rem", 
             'title':"date de naissance (jj/mm/aaa)"}))
    date_of_neuter = forms.DateField(required=False, 
        widget=forms.TextInput(attrs={ 
            'title' : "date de stérilisation",
            'placeholder' : "date de stérilisation ",
             "class":"w-10rem", 
             'title':"date de stérilisation (jj/mm/aaa)"}))
    file = forms.CharField(required=False,
        widget=forms.TextInput(attrs={ 'title' : "num du dossier",
            'placeholder' : "num du dossier"}))
    is_neutered = forms.ChoiceField(label="Stérile ? ", required=True, 
        widget=forms.RadioSelect(attrs={"class" : "lst-none pl-0"}), 
        choices=(CHOICE_STERIL))
    mail = forms.EmailField(required=True, max_length=30, 
        widget=forms.TextInput(attrs={ 'title' : 'mail' ,
            'placeholder' : "mail"}))
    mail_reminder = forms.IntegerField(required=True, 
        widget=forms.NumberInput(attrs={ 'title' : 'nb rappel mail' ,
            'placeholder' : "nb rappel mail",'min':0}))
    name = forms.CharField(required=True, label="Nom de l'animal", max_length=30, 
        widget=forms.TextInput(attrs={ 'title' : "nom de l'animal",
            'placeholder' : "nom de l'animal", "class":"w-10rem"}))
    status = forms.CharField(required=False, max_length=200, 
        widget=forms.Textarea(attrs={ 'title' : "statut de la stérilisation",
            'placeholder' : "statut de la stérilisation", 'cols':30, 'rows':3}))
       
    owner_name = forms.CharField(required=True, label="Prénom du propriétaire", max_length=30,
        widget=forms.TextInput(attrs={ 'title' : "propriétaire" ,
            'placeholder' : "prénom du propriétaire"}))
    owner_surname = forms.CharField(required=True, label="Nom du propriétaire", max_length=30,
        widget=forms.TextInput(attrs={ 'title' : "propriétaire" ,
            'placeholder' : "nom du propriétaire"}))
    owner_sexe = forms.ChoiceField(label="Sexe", required=True, 
        widget=forms.RadioSelect(attrs={'class' : 'li-oneline '}), choices=((1,"Homme"), (2,"Femme")))
    observation = forms.CharField(required=False, max_length=50, 
        widget=forms.TextInput(attrs={ 'title' : "observation(s)",
            'placeholder' : "observation(s)"}))
    color = forms.CharField(required=True, max_length=30, 
        widget=forms.TextInput(attrs={ 'title' : "couleur(s) de l'animal",
            'placeholder' : "couleur(s) de l'animal"}))
    race = forms.CharField(required=True, label="Race", max_length=30,
        widget=forms.TextInput(attrs={ 'title' : "race de l'animal" ,
            'placeholder' : "race de l'animal"}))
    species = forms.ChoiceField(widget=forms.RadioSelect(attrs={"class" : "lst-none pl-0"}), choices=CHOICES)
    tatoo = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={ 'title' : "num de tatouage" ,
            'placeholder' : "num de tatouage"}))
    phone = forms.CharField(required=True, max_length=15,
        widget=forms.TextInput(attrs={ 'title' : "téléphone",
            'placeholder' : "téléphone"}))
    tel_reminder = forms.IntegerField(required=True, 
        widget=forms.NumberInput(attrs={ 'title' : "nb rappel téléphonique",
            'placeholder' : "nb rappel tel",'min':0, "values":0}))

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
        animal.save()   
        return animal

    def _handle_admin_class(self, dict_values):
        #create and save admin classe
        list_admin = dict_values['admin']
        admin = AdminData(*list_admin)
        queryset = AdminData.objects.filter(chip=admin.chip,file=admin.file, tatoo=admin.tatoo)
        same_in_db = len(AdminData.objects.filter(chip=admin.chip,file=admin.file, tatoo=admin.tatoo)) > 0
        if same_in_db:
            return False, (f"Erreur : ce dossier admin existe déjà dans la base, risque de doublon, procédure annulée !")
        admin.save()
        return True, admin

    def _handle_owner_class(self, dict_values):
        #create and save owner classe
        #already exists ? 
        list_owner = dict_values['owner']
        owner_in_db = Owner.objects.filter(owner_name=list_owner[1], owner_surname=list_owner[2])
        if len(owner_in_db) != 0:
            owner = owner_in_db[0]
            return owner
        else:
            owner = Owner(*list_owner)
            try: 
                owner.save()
            except IntegrityError as ie: 
                raise ie
                if "tel" in str(ie):
                    PersonalErrorMsg("Ce téléphone existe déjà dans la base ! Procédure annulée ...")
                elif "mail" in str(ie):
                    PersonalErrorMsg("Ce mail existe déjà dans la base ! Procédure annulée ... ")
            except Exception as e: 
                raise e
            return owner

    def from_form(self):
        """ returns values to fill row in tables """
        animal = ('name', 'date_of_birth', 'race', 'species', 'color', 'date_of_adoption')
        admin = ('file', 'chip', 'tatoo', 'is_neutered', 'date_of_neuter', 'status')
        owner = ('owner_name', 'owner_surname','owner_sexe',  'phone', 'mail', 'tel_reminder', 'mail_reminder', 'caution')
        dict_values=self.cleaned_data

        # first element have to stay None because it is for id
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
        succes, output = self._handle_admin_class(dict_values)
        if succes:
            print('- données pour admin ok ')
            admin = output
        else:
            error_msg = output
            return error_msg
        try:
            owner = self._handle_owner_class(dict_values)
            print('- données pour owner ok ')
        except Exception as e:
            admin.delete()
            raise PersonalErrorMsg("Problème avec les données concernant owner, effacement données admin.")
        try:    
            animal = self._handle_animal_class(dict_values)
            animal.admin_data = admin
            animal.owner = owner
            animal.save()
            print('- données pour animal ok ')
            return 1
        except Exception as e:
            animal.delete()
            admin.delete()
            print('\t- erreur pour owner, effacement données admin et owner.')
            raise e
        


    """
        name_col = ('name','date_of_birth','race','species','color','date_of_adoption', 'picture')
    """