#python 
from datetime import datetime
from unittest import mock, skip

#from django
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

#from app
from .utils import Utils 
from .models import Mail
from .views import *

#from other apps
from sheet.models import Animal, AdminData, Owner

# class UnitTest(TestCase):
#     def setUp(self):
#       pass

def get_mail(nb):
  mails = []
  for time in range(nb):
      mail = Mail(title='mail'+str(time+1))
      mail.save()
      mails.append(mail)
  return mails

def get_one_sheet():
    """ create one sheet in db and return """
    admin = AdminData(
        is_neutered = 0, 
        file='123') #charfield
    admin.save()
    owner = Owner(
        owner_name = 'no name',
        owner_surname = 'Smith',
        owner_sex = 0,
        phone = '1234567890',
        mail = 'my@mail.com',
        caution = '0e',)
    owner.save()
    animal = Animal(
        name = "a",
        date_of_birth = datetime(2020,1,2).date(),
        race = 'bâtard',
        species = 0,
        color = 'grey',
        date_of_adoption = datetime.now())
    animal.save()
    animal.admin_data = admin
    animal.owner = owner
    animal.save()
    return (animal, admin, owner)


class TestMailView(TestCase):
    def setUp(self):
        self.mails = get_mail(3)

    def test_get_access_page(self):
        """this function tests whether user can access mail/index.html """
        response = self.client.get(reverse("mail:index"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_context_with_get(self): 
        """this function tests whether there are 3 mails in the context"""
        response = self.client.get(reverse("mail:index"), follow=True)
        mails = response.context['mails']
        self.assertEqual(len(mails), 3)

    def test_post_remove_mail(self):
        """this function tests if the post method remove mail from db
         corresponding to given mail_id 
            test : remove 2 mails if 2 mail_id
        """
        before = len(Mail.objects.all())
        #data pour retourner le request.POST dont j'ai besoin
        response = self.client.post(reverse("mail:index"), data={"checkbox":['1', '2']}, follow=True)
        after = len(Mail.objects.all())
        self.assertEqual(before, after + 2)


class TestCNSView(TestCase):
    def setUp(self):
        get_mail(3)

    def test_get_access_page(self):
        """this function tests whether user can access mail/index.html """
        response = self.client.get(reverse("mail:cns"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_access_page_with_mail_id(self):
        """this function tests whether user can access mail/index.html """
        #kwargs dans reverse pour obtenir l'url mail/cns/1
        response = self.client.get(reverse("mail:cns", kwargs={'mail_id':"1"}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mail'].mail_id, 1)



class TestContentView(TestCase):
    def setUp(self):
        self.mails = get_mail(3)
        get_one_sheet()

    def test_get_access_page(self):
        """this function tests whether user can access mail/add.html """
        response = self.client.get(reverse("mail:content"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_access_page_with_mail_id(self):
        """this function tests whether user can access mail/add.html with mail_id parameter"""

        response = self.client.get(reverse("mail:content", kwargs={'mail_id':"1"}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mail'].mail_id, 1)

    def test_content_when_mail_id(self):
        """this function tests whether user can access mail/add.html with mail_id parameter"""
        mail = self.mails[0]
        mail.resume = "test1"
        mail.full_text = "test2 : Bonjour **owner_sex** **owner_surname**"
        mail.save()
        response = self.client.get(reverse("mail:content", kwargs={'mail_id':"1"}), follow=True)
        # with open("data.txt", "w") as fichier:
        #     fichier.write(str(response.content))
        self.assertEqual(response.wsgi_request.get_full_path(), "/spa/mail/content/1")
        self.assertContains(response, "test1")
        self.assertContains(response, "test2 : Bonjour Monsieur Smith")

    def test_post_check_integrity(self): 
        """this function tests whether post can check integrity if Ajax request contains : 
            {'checkIntegrity' : "1", 'title':'mail1'} > output : {'problem':'1'} 
            {'checkIntegrity' : "1", 'title':'mail2'} > output : {'problem':'0'} 
        """
        datas1 = {'checkIntegrity' : "1", 'title':'mail1'}
        datas2 = {'checkIntegrity' : "1", 'title':'mail99'}

        response = self.client.post(reverse("mail:content"), data=datas1, follow=True)
        response2 = self.client.post(reverse("mail:content"), data=datas2, follow=True)
        #vérifie réponse Json du type : return JsonResponse({"problem" : "1"}, safe=False) 
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'problem': '1'})
        self.assertJSONEqual(str(response2.content, encoding='utf8'), {'problem': '0'})
    
    def test_post_add_new_mail(self): 
        """this function tests whether post can add new mail if client sends this : 
            {   
                'mail_id' : "None", 'title':'title',
                'resume': 'a resume', 'full_text' : 'content of the mail'
            } > output : add a new mail
        """
        datas = { 'title':'title','resume': 'a resume',
         'full_text' : 'content of the mail'}
        before = len(Mail.objects.all())
        response = self.client.post(reverse("mail:content"), data=datas, follow=True)
        after = len(Mail.objects.all())
        self.assertEqual(before + 1, after)

    def test_post_alter_mail(self):
        """this function tests whether post can alter a mail if client sends this : 
            {   
                'mail_id' : '1', 'title':'changed title',
                'resume': 'a resume', 'full_text' : 'content of the mail'
            } > output : alter a former mail
        """
        datas = {   
                    'mail_id' : '1', 'title':'changed title',
                    'resume': 'a resume', 'full_text' : 'content of the mail'
                }
        before = len(Mail.objects.all())
        former_title = Mail.objects.get(mail_id=1).title
        response = self.client.post(reverse("mail:content"), data=datas, follow=True)
        after = len(Mail.objects.all())
        new_title = Mail.objects.get(mail_id=1).title
        self.assertEqual(before, after) #no more mail
        self.assertFalse(former_title == new_title)

    def test_post_return_cns(self):
        """this function tests whether post can return to cns page if client sends this: 
            {   
                'mail_id' : '1', 'title':'changed title',
                'resume': 'a resume', 'full_text' : 'content of the mail', 
                'overview' : 0,
            } > output : redirect to cns page 
            """
        datas = {   
                    'mail_id' : '1', 'title':'changed title',
                    'resume': 'a resume', 'full_text' : 'content of the mail',
                    'overview' : '0',
                }

        response = self.client.post(reverse("mail:content"), data=datas, follow=True)
        print(response.context['mail'])
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, reverse("mail:cns"))

    def test_post_return_jsresponse_overview(self):
        """this function tests whether post can return to cns page if client sends this: 
            {   
                'mail_id' : '1', 'title':'changed title',
                'resume': 'a resume', 'full_text' : 'content of the mail', 
                'overview' : 0,
            } > output : redirect to cns page 
            """
        datas = {   
                    'mail_id' : '1', 'title':'changed title',
                    'resume': 'a resume', 'full_text' : 'content of the mail',
                    'overview' : '1',
                }

        response = self.client.post(reverse("mail:content"), data=datas, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"mail_id" : '1'})


class TestOverviewView(TestCase):
    def setUp(self):
        self.mails = get_mail(1)
        get_one_sheet() 

    def test_overview_content_when_mail_id(self):
        """this function tests whether user can access mail/add.html with mail_id parameter"""
        mail = self.mails[0]
        mail.resume = "test1"
        mail.full_text = "test2 : Bonjour **owner_sex** **owner_surname**"
        mail.save()
        response = self.client.get(reverse("mail:overview", kwargs={'mail_id':"1"}), follow=True)
        self.assertEqual(response.wsgi_request.get_full_path(), "/spa/mail/overview/1/")
        self.assertContains(response, "test1")
        self.assertContains(response, "test2 : Bonjour Monsieur Smith")

      
class TestSettingsView(TestCase):
    def setUp(self):
        self.mails = get_mail(3)
        patcher = mock.patch("sheet.views.SheetForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value
    
    def test_get_access_page(self):
        """this function tests whether user can access mail/add.html """
        response = self.client.get(reverse("mail:settings"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_access_page_with_mail_id(self):
        """this function tests whether user can access mail/add.html with mail_id parameter"""

        response = self.client.get(reverse("mail:settings", kwargs={'mail_id':"1"}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mail'].mail_id, 1)
        
    def test_post_data_received_ajax_1(self):
        """ this function tests whether mail.auto changes when received datas with: 
            {"ajax" : "1"}
        """
        datas = {
            "ajax" : "1", "mail_id" : "1", "auto_send" : "1"
        }
        before = Mail.objects.get(mail_id=1).auto_send
        print(8888)
        print(before)
        response = self.client.post(reverse("mail:settings"), data=datas, follow=True)
        after = Mail.objects.get(mail_id=1).auto_send
        send_after_creation = Mail.objects.get(mail_id=1).send_after_creation
        print(after)
        self.assertTrue(before != after)
        self.assertTrue(send_after_creation)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"chgt" : "saved"})

    def test_post_form_is_valid(self): 
        """this function tests whether getattr(mail, given param]) change if I change the received datas
            according to what can be send by client
        """
        self.mock_form.is_valid.return_value= True
        tab = ['send_after_creation', 'send_after_modif', 'send_when_x_month', 'send_at_this_date']
        for number in range(4):
            res = str(number+1)
            datas = {"frequency" : res}
            if res == "3": 
                datas["age"] = 6
            elif res == "4":
                datas["date"] = '22/02/1991'
            print("-----------------------------------------------")
            print("data : ", datas, number)
            mail = Mail.objects.get(mail_id="1")
            before = getattr(mail, tab[number])
            print(f"\tauto save : {mail.auto_send} | {tab[number]} : {getattr(mail, tab[number])}")
            response = self.client.post(reverse("mail:settings", kwargs={'mail_id':"1"}), 
                data=datas, follow=True)
            mail = Mail.objects.get(mail_id="1")
            after = getattr(mail, tab[number])
            self.assertTrue(response.status_code, 200)
            self.assertTrue(before != after)
            print(f"\tauto save : {mail.auto_send} | {tab[number]} : {getattr(mail, tab[number])}")
            print("fin")



