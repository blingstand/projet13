from .models import *
from datetime import date
""" script for the needed form"""
from django import forms
CHOICES = (
    ("1", "chat"),("2", "chatte"), ("3", "chien"), ("4", "chienne"))

class DateInput(forms.DateInput):
    input_type = 'date'
class SheetForm(forms.Form):
    """form to add a new sheet """
    caution = forms.CharField(required=True, max_length=30, 
        widget=forms.TextInput(attrs={ 
            'title' : 'montant de la caution',
            'placeholder' : "montant de la caution"}))
    chip = forms.IntegerField(required=False,  
        widget=forms.TextInput(attrs={ 'title' : 'num de la puce',
            'placeholder' : "num de la puce"}))
    date_of_adoption = forms.DateField(required=False, 
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date d'adoption ",
             "class":"w-10rem", 
             'title':"date d'adoption (jj/mm/aaa)"}))
    date_of_birth = forms.DateField(required=False, 
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
    file = forms.IntegerField(required=False,
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
       
    owner = forms.CharField(required=True, label="Nom du propriétaire", max_length=30,
        widget=forms.TextInput(attrs={ 'title' : "propriétaire" ,
            'placeholder' : "propriétaire"}))
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
    tatoo = forms.IntegerField(required=False, 
        widget=forms.TextInput(attrs={ 'title' : "num de tatouage" ,
            'placeholder' : "num de tatouage"}))
    tel = forms.CharField(required=True, max_length=15,
        widget=forms.TextInput(attrs={ 'title' : "téléphone",
            'placeholder' : "téléphone"}))
    tel_reminder = forms.IntegerField(required=False, 
        widget=forms.NumberInput(attrs={ 'title' : "nb rappel téléphonique",
            'placeholder' : "nb rappel tel",'min':0}))

    def from_form(self):
        """ returns values to fill row in tables """
        animal = ('name', 'date_of_birth', 'race', 'species', 'color', 'date_of_adoption')
        admin = ('file', 'chip', 'tatoo', 'is_neutered', 'date_of_neuter', 'status')
        owner = ('owner', 'tel', 'mail', 'tel_reminder', 'mail_reminder', 'caution')
        
        dict_values=self.cleaned_data

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
        """ save the data in database """
        
        #create classes 
        list_owner = dict_values['owner']
        owner = Owner(*list_owner)
        list_admin = dict_values['admin']
        admin = AdminData(*list_admin)
        list_ani = dict_values['animal']
        animal = Animal(*list_ani)

        # #save classes
        admin.save()
        animal.save()
        owner.save()
        # # #add foreignKey
        # animal.admin_data_id.add(admin)
        # animal.owner_id.add(owner)
        # animal.save()
        


    """
        name_col = ('name','date_of_birth','race','species','color','date_of_adoption', 'picture')
    """