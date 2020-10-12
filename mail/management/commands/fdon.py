#from python
from datetime import datetime

#from django
from django.db.models import Q
""" this script drop datas from tables Category and Product"""
from django.core.management.base import BaseCommand

from sheet.models import *
from mail.models import Mail

class Command(BaseCommand):
    """ this class manages the parameters you can pass to python manage.py"""
    help = "this command displays the name of animal and the futur date fo their neuter"

    def _fdon(self):
        """drops the datas"""
        print(f"Mission du {datetime.now().date()}: ")
        print(f"Je dois envoyer un mail à : ")
        admins = AdminData.objects.filter(
            futur_date_of_neuter=datetime.now().date())
        if admins:
            for admin in admins:
                anim = Animal.objects.filter(admin_data=admin)[0]
                if anim: 
                    print(f"- {anim.owner.owner_name} {anim.owner.owner_surname} pour lui dire "\
                    f"que son/sa {anim.str_species} {anim.name} peut maintenant être stérilisé.")
                    print(f"Je vais utiliser cette adresse mail : {anim.owner.mail}")
        mail = Mail.objects.filter(send_when_neuterable=True)
        mail = Mail.objects.all()
        print(mail)
        if mail : 
            print(f"Je vais utiliser ce modèle de mail : {mail[0].title}")
            print(f'\trésumé :', mail[0].resume)
            print(f'\tcontenu :', mail[0].modified_text(anim.id))
            mail[0].send_auto_mail(anim.owner.mail, anim.id)

    def handle(self, *args, **options):
        """throws the drop_db function"""
        print("\n", "* "*30)
        self._fdon() 
        print("\n", "* "*30, "\n")