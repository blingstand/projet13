#from python
from datetime import datetime

#from django
from django.db.models import Q
""" this script drop datas from tables Category and Product"""
from django.core.management.base import BaseCommand

from sheet.models import  *
from mail.models import Mail

recall_days = 1, 15

class Command(BaseCommand):
    """ this class manages the parameters you can pass to python manage.py"""
    help = "this daily command send a mail to the whole list of contact if current"\
     "day is 1st or 15th"

    def _2weeks(self): 
        """drops the datas"""
        day = datetime.now().day
        print(f"Vérification de la date : {datetime.now().date()}: ")
        print(f"day : {day} ")
        
        if day in recall_days: 
        	print("C'est le jour de relance")
        	owners = [owner for owner in Owner.objects.all() if owner.has_rdy_to_neuter_animals]
        	print(f'Je vais contacter : {owners}')

        mail = Mail.objects.get(condition=Mail.E2W, auto_send=True)
        print(mail)
        if mail : 
            print(f"Je vais utiliser ce modèle de mail : {mail.title}")
            print(f'\trésumé :', mail.resume)
            print(f'\tcontenu :', mail.modified_text())
            for owner in owners:
            	for animal in owner.get_list_animal:
            		mail.send_auto_mail(owner.mail, animal.id)
        

    def handle(self, *args, **options):
        """throws the drop_db function"""
        print("\n", "* "*30)
        self._2weeks() 
        print("\n", "* "*30, "\n")