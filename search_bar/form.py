from django import forms

class SearchForm(forms.Form):
    """form to add a new mail content"""
    search_input = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={ 'class' : "w-100 text-left pl-3",
            'placeholder' : "recherche rapide. ex >> prop:DUPONT", 'autocomplete':"off"}))