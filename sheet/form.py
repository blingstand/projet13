""" script for the needed form"""

from datetime import date

from django import forms
from django.db.utils import IntegrityError

from .models import *

CHOICES = (
    ("1", "chat"),("2", "chatte"), ("3", "chien"), ("4", "chienne"))

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
        widget=forms.RadioSelect, choices=((True,"oui"), (False,"non")))
    mail = forms.EmailField(required=True, max_length=30, 
        widget=forms.TextInput(attrs={ 'title' : 'mail' ,
            'placeholder' : "mail"}))
    mail_reminder = forms.IntegerField(required=False, 
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
    species = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    tatoo = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={ 'title' : "num de tatouage" ,
            'placeholder' : "num de tatouage"}))
    phone = forms.CharField(required=True, max_length=15,
        widget=forms.TextInput(attrs={ 'title' : "téléphone",
            'placeholder' : "téléphone"}))
    tel_reminder = forms.IntegerField(required=False, 
        widget=forms.NumberInput(attrs={ 'title' : "nb rappel téléphonique",
            'placeholder' : "nb rappel tel",'min':0, "values":0}))

    def _handle_animal_class(self, dict_values):
        #create and save animal classe
        list_ani = dict_values['animal']
        animal = Animal(*list_ani)  
        animal.save()   
        return animal

    def _handle_admin_class(self, dict_values):
        #create and save admin classe
        list_admin = dict_values['admin']
        admin = AdminData(*list_admin)
        found_file = AdminData.objects.filter(file=admin.file)
        found_chip = AdminData.objects.filter(chip=admin.chip)
        found_tatoo = AdminData.objects.filter(tatoo=admin.tatoo)
        for elem in [found_file, found_chip, found_tatoo]:
            if len(elem) > 0:
                PersonalErrorMsg(f"{elem} existe déjà dans la base, risque de doublon, procédure annulée !")
        admin.save()
        return admin

    def _handle_owner_class(self, dict_values):
        #create and save owner classe
        #already exists ? 
        list_owner = dict_values['owner']
        owner = Owner.objects.filter(owner_name=list_owner[1], owner_surname=list_owner[2])
        if len(owner) is not 0:
            print("Cet utilisateur existe déjà !")
        else:
            print("Cet utilisateur est nouveau !")
        owner = Owner(*list_owner)
        try: 
            owner.save()
        except IntegrityError as ie: 
            raise ie
            if "tel" in str(ie):
                PersonalErrorMsg("Ce téléphone est existe déjà dans la base ! Procédure annulée ...")
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
        try : 
            animal = self._handle_animal_class(dict_values)
            print('ani ok ')
        except Exception as e:
            raise e
        try:
            admin = self._handle_admin_class(dict_values)
            print('admin ok ')
        except Exception as e:
            animal.delete()
            raise e
            
        try:    
            owner = self._handle_owner_class(dict_values)
            print('owner ok ')
            animal.admin_data = admin
            animal.owner = owner
            animal.save()
            print('ani2 ok ')
            return 1
        except Exception as e:
            animal.delete()
            admin.delete()
            raise e
        


    """
        name_col = ('name','date_of_birth','race','species','color','date_of_adoption', 'picture')
    """