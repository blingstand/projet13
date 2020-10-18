""" script for the needed form"""
#from python
from datetime import datetime

#from django
from django import forms

#from other app
from mail.mail_manager import MailManager

#from current app
from .models import Animal, AdminData, Owner
from .utils import UtilsSheet
ut = UtilsSheet()
mm = MailManager()
CHOICES = (
    ("0", "chat"),("1", "chatte"), ("2", "chien"), ("3", "chienne"))
CHOICE_STERIL = ("0","stérilisé"), ("1","stérilisable"), ("2","sera stérilisable")
CHOICE_SEX = (("0","Homme"), ("1","Femme"))
CHOICES_NATURE = (("0", "mail automatique"),("1", "mail spa"), ("2", "tel spa"), \
    ("3", "mail propriétaire"), ("4", "tel propriétaire"))
CHOICES_CAUTION = ("0","chèque"), ("1","virement"), ("2","espèces")

class SheetForm(forms.Form):
    """form to add a new sheet """
    caution = forms.IntegerField(required=True, label='caution', initial='100',
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced',
            'title' : 'montant de la caution',
            'placeholder' : "montant (sans €)"}))
    chip = forms.CharField(required=False,  label='puce',
        widget=forms.TextInput(attrs={ 'class' : 'w-10rem', 'title' : 'num de la puce',
            'placeholder' : "num de la puce", 'maxlength':"15"}))
    color = forms.CharField(required=True, max_length=30, label='Couleur',
        widget=forms.TextInput(attrs={ 'class' : 'w-10rem', 'title' : "couleur(s) de l'animal",
            'placeholder' : "couleur(s)"}))
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
    is_neutered = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={"class" : "li-oneline align-left lst-none pl-0 mb-0"}),
        choices=(CHOICE_STERIL))
    select_owner= forms.CharField(required=False)
    mail = forms.EmailField(required=False, max_length=30, label='mail',
        widget=forms.EmailInput(attrs={'class' : 'text-center', 'title' : 'mail' ,
            'placeholder' : "mail", 'name' : 'mail'}))
    mail_reminder = forms.IntegerField(required=False, label='nb mail',initial='0',
        widget=forms.NumberInput(attrs={
            'class' : 'input-very-reduced', 'title' : 'nb rappel mail' ,
            'placeholder' : "nb rappel mail",'min':0}))
    name = forms.CharField(required=True, label="Nom de l'animal", max_length=30,
        widget=forms.TextInput(attrs={ 'title' : "nom de l'animal",
            'placeholder' : "nom de l'animal", "class":"w-10rem"}))
    nature_caution = forms.CharField(required=True, label="nature : ", max_length=20,
        widget=forms.Select(attrs={ 'title' : "Nature de la caution",
            "class":"w-10rem"}, choices=CHOICES_CAUTION))
    status = forms.CharField(required=False, max_length=200,
        widget=forms.Textarea(attrs={ 'title' : "statut de la stérilisation",
            'placeholder' : "statut de la stérilisation", 'cols':55, 'rows':2, 'class':'mb-3'}))
    owner_name = forms.CharField(required=False, label="prénom", max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "propriétaire" ,
            'placeholder' : "prénom proprio", 'name':"Prénom"}))
    owner_surname = forms.CharField(required=False, label="nom", max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "propriétaire" ,
            'placeholder' : "nom proprio", 'name':"Nom"}))
    owner_sex = forms.ChoiceField(label="Sexe", required=False,
        widget=forms.RadioSelect(attrs={
            'class' : 'li-oneline very-center', 'name':"Sexe"}), choices=CHOICE_SEX)
    # observation = forms.CharField(required=False, max_length=50, label='observation(s)',
    #     widget=forms.TextInput(attrs={ 'title' : "observation(s)",
            # 'placeholder' : "observation(s)"}))
    phone = forms.CharField(required=False, max_length=15, label='tel',
        widget=forms.TextInput(attrs={
            'class' : 'input-reduced', 'title' : "téléphone",'name':"Téléphone",
            'placeholder' : "téléphone"}))
    race = forms.CharField(required=True, label="race", max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'w-10rem', 'title' : "race de l'animal" ,
            'placeholder' : "race de l'animal"}))
    species = forms.ChoiceField(widget=forms.Select(attrs={"class" : "w-10rem lst-none pl-0",
        'onchange':'clickSelectedOption(this)'}), choices=CHOICES)
    tatoo = forms.CharField(required=False, label='tatouage',
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', 'title' : "num de tatouage" ,
            'placeholder' : "num de tatouage"}))
    tel_reminder = forms.IntegerField(required=False, label='nb appel', initial='0',
        widget=forms.NumberInput(attrs={
            'class' : 'input-very-reduced', 'title' : "nb rappel téléphonique",
            'placeholder' : "nb rappel tel",'min':0, "values":0}))
    def _handle_admin_class(self, dict_values):
        """create admin classe"""
        list_admin = [elem if elem != "None" else None for elem in dict_values['admin']]
        admin = AdminData(*list_admin)
        same_in_db = len(AdminData.objects.filter(
            chip=admin.chip,
            file=admin.file,
            tatoo=admin.tatoo)) > 0
        if same_in_db:
            return False, f"Erreur : ce dossier admin existe déjà dans la base,"\
            " risque de doublon, procédure annulée !"
        return True, admin
    def _handle_owner_class(self, dict_values):
        """get concerned owner"""
        owner = Owner.objects.get(id=dict_values["owner"])
        return True, owner
    def _handle_animal_class(self, dict_values):
        """create animal classe if animal doesn"t already exists"""
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
        animal = ('name', 'date_of_birth', 'race', 'species', 'color', \
            'date_of_adoption', 'caution', 'nature_caution')
        admin = ('file', 'chip', 'tatoo', 'is_neutered', 'date_of_neuter', \
            'futur_date_of_neuter', 'status')
        dict_values=self.cleaned_data
        print("00 >", dict_values['select_owner'])
        # first element have to stay None because it is for auto-id
        animal = [None] + [dict_values[elem] for elem in animal]
        owner = dict_values['select_owner']
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
                "full_text": f"félicitation adoption de {animal.name}({animal.str_species})"\
                " + rappel loi sur stérilisation"
            }
            owner.mail_reminder = str(int(owner.mail_reminder) + 1)
            success, output = mm.create_contact(owner, data)
            return success, output
        except Exception as exc:
            return False, f"problème dans create_first_contact : {exc}"
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
        except Exception as exc:
            print("***")
            print("ERROR admin: ", exc)
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
        except Exception:
            admin.delete()
            return "erreur pour owner, effacement données admin", None
        try:
            success3, output = self._handle_animal_class(dict_values)
            if success3:
                print(f"output : {output}")
                animal = output
                animal.admin_data = admin
                animal.owner = owner
                animal.name = animal.name.upper()
                animal.save()
                # print('- données pour animal ok ')
            else:
                admin.delete()
                response = self.is_owner_unique(owner)
                if response:
                    owner.delete()
                    print('\t- erreur pour animal, effacement données animal,"\
                        " admin et owner (unique).')
                else:
                    print('\t- erreur pour owner, effacement données animal et "\
                        "admin, owner (pas unique).')
                error_msg = output
                return error_msg, None
        except Exception as exc:
            raise exc
        success4, output = self.create_first_contact(owner, animal)
        print(f"création 1er contact")
        if success4:
            return  1, animal
        admin.delete()
        response = self.is_owner_unique(owner)
        if response:
            owner.delete()
            print('\t- erreur pour animal, effacement données animal, "\
                "admin et owner (unique).')
        else:
            print('\t- erreur pour owner, effacement données animal et "\
                "admin, owner (pas unique).')
        error_msg = output
        return error_msg, None

class JustOwnerForm(forms.Form):
    """form designed for owner add and alter"""
    owner_name = forms.CharField(required=True, label="Prénom", max_length=30,\
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', \
            'title' : "propriétaire" ,'name':"Prénom"}))
    owner_surname = forms.CharField(required=True, label="Nom", max_length=30,\
        widget=forms.TextInput(attrs={ 'class' : 'input-reduced', \
            'title' : "propriétaire" ,'name':"Nom"}))
    owner_sex = forms.ChoiceField(label="Sexe", required=True,\
        widget=forms.RadioSelect(attrs={'class' : 'li-oneline very-center', 'name':"Sexe"}),
        choices=CHOICE_SEX)
    mail = forms.EmailField(required=True, max_length=30, label='Mail',
            widget=forms.EmailInput(attrs={'class' : 'text-center', 'title' : 'mail' ,
                'name' : 'mail'}))
    phone = forms.CharField(required=True, max_length=15, label='Tel',
            widget=forms.TextInput(attrs={ 'class' : 'input-reduced',
                'title' : "téléphone",'name':"Téléphone"}))
