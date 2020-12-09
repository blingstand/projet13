from datetime import date

from django import forms
from django.db.utils import IntegrityError

from .models import *

CHOICES = (
    ("1", "à la création de la fiche,"),
    ("2", "quand je modifie la valeur de la caution,"), 
    ("3", "à la suppression d'une fiche,"),
    ("4", "toutes les deux semaines,(fonctionalité à vernir)"),
    ("5", "quand l'animal devient stérilisable."))

class SettingsMail(forms.Form):
    """form to add a new mail rule"""
    frequency = forms.ChoiceField(widget=forms.RadioSelect(attrs={"class":"lst-none"}), choices=CHOICES)

class ContentMail(forms.Form):
    """form to add a new mail content"""
    title = forms.CharField(max_length=30, label="titre",
        widget=forms.TextInput(attrs={ 'class' : "w-100 text-center blank",
            'placeholder' : "titre du mail"}))
    resume = forms.CharField(max_length=100, label="objet", 
        widget=forms.TextInput(attrs={ 'class' : "w-100 text-center blank",
            'placeholder' : "objet "}))
    plain_text = forms.CharField(max_length=4000, label="contenu",
        widget=forms.Textarea(attrs={ 
            'id':'plain_text',
            'class' : "w-100 blank p-3 text-justify",
            'rows': 20,
            'placeholder' : "contenu du mail, pensez à utiliser les touches sur les côtés"}))

    
