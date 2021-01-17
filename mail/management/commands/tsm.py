#from python
from datetime import datetime
import os

#from django
from django.db.models import Q
""" this script drop datas from tables Category and Product"""
from django.core.management.base import BaseCommand

from sheet.models import  *
from mail.models import Mail

from django.core.mail import send_mail


class Command(BaseCommand):
    """ this class manages the parameters you can pass to python manage.py"""
    help = "this daily command send a mail to the whole list of contact if current"\
     "day is 1st or 15th"

    def _test_send_mail(self): 
        """drops the datas"""
        day = datetime.now().day
        print("***")
        print("Cette commande envoie un mail à adrien.clupot@gmail.com pour tester les paramètres sendGrid")
        animal = Animal.objects.all()[0]
        subject = "Ceci est un test"
        if os.environ.get('ENV') == 'PRODUCTION':
            subject = "Ceci est un test envoyé depuis heroku"
        send_mail(
            subject= subject,
            message=None ,
            from_email='blingstand@hotmail.fr',
            recipient_list=['adrien.clupot@gmail.com'],
            html_message="réussite !! ", fail_silently=False
        )
        print("***")

    def handle(self, *args, **options):
        """throws the drop_db function"""
        print("\n", "* "*30)

        self._test_send_mail() 
        print("\n", "* "*30, "\n")