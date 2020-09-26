from datetime import date

from django import forms
from django.db.utils import IntegrityError

from .models import *

CHOICES = (
    ("1", "à la création de la fiche"),
    ("2", "quand je modifie la valeur de la caution"), 
    ("3", "quand l'animal a plus de"),
    ("4", "à cette date : jj/mm/aaaa"))

class DateInput(forms.DateInput):
    input_type = 'date'
class SettingsMail(forms.Form):
    """form to add a new mail rule"""
    frequency = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    age = forms.IntegerField(required=False)
    date = forms.DateField(required=False)

class ContentMail(forms.Form):
    """form to add a new mail content"""
    title = forms.CharField(max_length=30, label="titre",
        widget=forms.TextInput(attrs={ 'class' : "w-100 text-center blank",
            'placeholder' : "titre du mail"}))
    resume = forms.CharField(max_length=100, label="objet", 
        widget=forms.TextInput(attrs={ 'class' : "w-100 text-center blank",
            'placeholder' : "objet "}))
    full_text = forms.CharField(max_length=2000, label="contenu",
        widget=forms.Textarea(attrs={ 
            'id':'body_mail',
            'class' : "w-100 blank pl-3 pr-3",
            'placeholder' : "contenu du mail, pensez à utiliser les touches sur les côtés"}))

    