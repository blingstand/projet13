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
        widget=forms.TextInput(attrs={ 'placeholder' : "montant de la caution"}))
    chip = forms.IntegerField(required=False,  
        widget=forms.TextInput(attrs={ 'placeholder' : "num de la puce"}))
    date_of_adoption = forms.DateField(required=False, 
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date d'adoption ",
             "class":"w-10rem", 
             'title':'jj/mm/aaa'}))
    date_of_birth = forms.DateField(required=False, 
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date de naissance ",
             "class":"w-10rem", 
             'title':'jj/mm/aaa'}))
    date_of_neuter = forms.DateField(required=False, 
        widget=forms.TextInput(attrs={ 
            'placeholder' : "date de stérilisation ",
             "class":"w-10rem", 
             'title':'jj/mm/aaa'}))
    file = forms.IntegerField(required=False,
        widget=forms.TextInput(attrs={ 'placeholder' : "num du dossier"}))
    is_neutered = forms.ChoiceField(label="Stérile ? ", required=True, 
        widget=forms.RadioSelect, choices=(("1","oui"), ("2","non")))
    mail = forms.EmailField(required=True, max_length=30, 
        widget=forms.TextInput(attrs={ 'placeholder' : "mail"}))
    mail_reminder = forms.IntegerField(required=False, 
        widget=forms.NumberInput(attrs={ 'placeholder' : "nb rappel mail",'min':0}))
    name = forms.CharField(required=True, label="Nom de l'animal", max_length=30, 
        widget=forms.TextInput(attrs={ 'placeholder' : "nom de l'animal", "class":"w-10rem"}))
    status = forms.CharField(required=False, max_length=200, 
        widget=forms.Textarea(attrs={ 'placeholder' : "statut de la stérilisation", 'cols':30, 'rows':3}))
       
    owner = forms.CharField(required=True, label="Nom du propriétaire", max_length=30,
        widget=forms.TextInput(attrs={ 'placeholder' : "propriétaire"}))
    observation = forms.CharField(required=False, max_length=50, 
        widget=forms.TextInput(attrs={ 'placeholder' : "observation"}))
    color = forms.CharField(required=True, max_length=30, 
        widget=forms.TextInput(attrs={ 'placeholder' : "couleur de l'animal"}))
    race = forms.CharField(required=True, label="Race", max_length=30,
        widget=forms.TextInput(attrs={ 'placeholder' : "race de l'animal"}))
    species = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    tatoo = forms.IntegerField(required=False, 
        widget=forms.TextInput(attrs={ 'placeholder' : "num de tatouage"}))
    tel = forms.CharField(required=True, max_length=15,
        widget=forms.TextInput(attrs={ 'placeholder' : "téléphone"}))
    tel_reminder = forms.IntegerField(required=False, 
        widget=forms.NumberInput(attrs={ 'placeholder' : "nb rappel tel",'min':0}))

    def from_form(self):
        """ returns values to fill row in tables """
        animal = ('name', 'date_of_birth', 'race', 'species', 'color', 'date_of_adoption')
        admin = ('chip', 'file', 'tatoo', 'is_neutered', 'date_of_neuter', 'status')
        owner = ('owner', 'tel', 'mail', 'tel_reminder', 'mail_reminder', 'caution')
        
        dict_values=self.cleaned_data

        animal = [None] + [dict_values[elem] for elem in animal]
        admin = [dict_values[elem] for elem in admin]
        owner = [dict_values[elem] for elem in owner]
        print(f"animal value = {animal}")
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

        #save classes
        animal.save()
        owner.save()
        admin.save()
        # #add foreignKey
        animal.admin_data_id.add(admin)
        animal.owner_id.add(owner)
        animal.save()
        


    """
        name_col = ('name','date_of_birth','race','species','color','date_of_adoption', 'picture')
    """