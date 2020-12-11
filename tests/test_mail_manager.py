#python 
from datetime import datetime
from unittest import mock, skip

#from django
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

#from app
from mail.utils import UtilsMail
from mail.models import Mail
from mail.views import *
from mail.data import change_date_format as cdf
from mail.mail_manager import MailManager


#from other apps
from sheet.models import Animal, AdminData, Owner


@skip
class TestMailManager(TestCase):

	def setUp(self):
		for i in range(6):
			mail = Mail(title=f"test{i}", condition=i)
			mail.save()

	def test_has_to_send_mail(self):
		mm = MailManager()
		mm.has_to_send_mail(Mail.CAS)
