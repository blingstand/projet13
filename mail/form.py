from datetime import date

from django import forms
from django.db.utils import IntegrityError

from .models import *


CHOICES = Mail.str_condition_form_choices()
class SettingsMail(forms.ModelForm):
    class Meta: 
        model = Mail
        fields = ('condition', )
        widgets = {
        'condition': forms.RadioSelect(choices=CHOICES),
        }
        """form to add a new mail rule"""
    # frequency = forms.ChoiceField(widget=forms.RadioSelect(attrs={"class":"lst-none"}), choices=CHOICES)

class ContentMail(forms.Form):
    """form to add a new mail content"""
    title = forms.CharField(max_length=100, label="titre",
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

        
