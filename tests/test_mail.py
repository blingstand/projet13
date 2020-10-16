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
        phone = '0234567890',
        mail = 'my@mail.com',
        )
    owner.save()
    animal = Animal(
        name = "a",
        date_of_birth = datetime(2020,1,2).date(),
        race = 'bâtard',
        species = 0,
        color = 'grey',
        caution = '0',
        date_of_adoption = datetime.now())
    animal.save()
    animal.admin_data = admin
    animal.owner = owner
    animal.save()
    return (animal, admin, owner)

class TestMailModels(TestCase):

    def test_get_condition(self): 
        """test if returns str_condition when auto_send == True"""
        get_mail(1)
        mail = Mail.objects.all()[0]
        self.assertEqual(mail.get_condition(), None)
        print("**********")
        mail.auto_send = True
        mail.send_after_creation = True
        is_str = mail.get_condition()
        self.assertTrue(isinstance(is_str, str))

class TestMailData(TestCase):
    
    def test_change_date_format(self):
        """test if returns a str when a datetime is given"""
        date = datetime.now().date()
        is_str = cdf(date)
        self.assertTrue(isinstance(is_str, str))

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
        print('**********')
        print(len(mails))
        self.assertEqual(len(mails), 3)

    def test_post_remove_mail(self):
        """this function tests if the post method remove mail from db
         corresponding to given mail_id 
            test : remove 2 mails if 2 mail_id
        """
        before = len(Mail.objects.all())
        #data pour retourner le request.POST dont j'ai besoin
        given_id  = Mail.objects.all()[0].mail_id
        response = self.client.post(reverse("mail:index"), data={"checkbox":[given_id]}, follow=True)
        after = len(Mail.objects.all())
        self.assertEqual(before, after + 1)


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
        all_mails = Mail.objects.all()
        kwargs = { 'mail_id':all_mails[0].mail_id}
        response = self.client.get(reverse("mail:cns", kwargs=kwargs), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mail'].mail_id, kwargs['mail_id'])


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
        all_mails= Mail.objects.all()
        response = self.client.get(reverse("mail:content", kwargs={'mail_id':all_mails[0].mail_id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mail'].mail_id,all_mails[0].mail_id)

    def test_content_when_mail_id(self):
        """this function tests whether user can access mail/add.html with mail_id parameter"""
        mail = self.mails[0]
        all_mails= Mail.objects.all()
        given_id = all_mails[0].mail_id
        mail.resume = "test1"
        mail.plain_text = "test2 : Bonjour **M./Mme** **nom prop**"
        mail.save()
        response = self.client.get(reverse("mail:content", kwargs={'mail_id':given_id}), follow=True)
        # with open("data.txt", "w") as fichier:
        #     fichier.write(str(response.content))
        self.assertEqual(response.wsgi_request.get_full_path(), f"/spa/mail/content/{given_id}")
        self.assertContains(response, "test1")
    

    def test_post_check_integrity(self): 
        """this function tests whether post can check integrity if Ajax request contains : 
            {'checkIntegrity' : "1", 'title':'mail1'} > output : {'problem':'1'} 
            {'checkIntegrity' : "1", 'title':'mail2'} > output : {'problem':'0'} 
        """
        kwargs = {'action' : "check_integrity", 'mail_id':'1'}
        datas1 = {'title' : "mail1"}
        datas2 = {'title' : "mail20"}

        response = self.client.post(reverse("mail:content", kwargs=kwargs), data=datas1, follow=True)
        response2 = self.client.post(reverse("mail:content", kwargs=kwargs), data=datas2, follow=True)
        #vérifie réponse Json du type : return JsonResponse({"problem" : "1"}, safe=False) 
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'data': '1'})
        self.assertJSONEqual(str(response2.content, encoding='utf8'), {'data': '0'})

    def test_post_add_new_mail(self): 
        """this function tests whether post can add new mail if client sends this : 
            {   
                'mail_id' : "None", 'title':'title',
                'resume': 'a resume', 'plain_text' : 'content of the mail'
            } > output : add a new mail
        """
        datas = { 'title':'title','resume': 'a resume',
         'plain_text' : 'content of the mail'}
        before = len(Mail.objects.all())
        response = self.client.post(reverse("mail:content"), data=datas, follow=True)
        after = len(Mail.objects.all())
        self.assertEqual(before + 1, after)

    def test_post_alter_mail(self):
        """this function tests whether post can alter a mail if client sends this : 
            kwargs, datas > output : alter a former mail
        """
        all_mails = Mail.objects.all()
        before = len(all_mails)
        kwargs = { 'mail_id':all_mails[0].mail_id}
        datas = {   
                    'title':'changed title',
                    'resume': 'a resume', 'plain_text' : 'content of the mail'
                }
        former_title = Mail.objects.get(mail_id=kwargs['mail_id']).title
        response = self.client.post(reverse("mail:content", kwargs=kwargs), data=datas, follow=True)
        after = len(Mail.objects.all())
        new_title = Mail.objects.get(mail_id=kwargs['mail_id']).title
        self.assertEqual(before, after) #no more mail
        self.assertFalse(former_title == new_title)

    def test_post_return_cns(self):
        """this function tests whether post can return to cns page if client sends this: 
            kwargs, datas > output : redirect to cns page 
            """
        all_mails = Mail.objects.all()
        kwargs = { 'mail_id':all_mails[0].mail_id,}
        datas = {   
                    'title':'changed title',
                    'resume': 'a resume', 'plain_text' : 'content of the mail',
                }

        response = self.client.post(reverse("mail:content", kwargs=kwargs), data=datas, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.get_full_path(), f"/spa/mail/cns/{kwargs['mail_id']}")

    def test_post_return_jsresponse_overview(self):
        """this function tests whether post can return to cns page if client sends this: 
            {   
                'title':'changed title',
                'resume': 'a resume', 'plain_text' : 'content of the mail'
            } > output : redirect to cns page 
            """
        all_mails = Mail.objects.all()
        # print('test all_mails : ', [mail.mail_id for mail in all_mails])
        kwargs = { 'mail_id':all_mails[0].mail_id, 'action':'overview'}
        datas = {   
                    'title':'changed title',
                    'resume': 'a resume', 'plain_text' : 'content of the mail'
                }

        response = self.client.post(reverse("mail:content", kwargs=kwargs), data=datas, follow=False)
        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(str(response.content, encoding='utf8'), {"data" : kwargs['mail_id']})


class TestOverviewView(TestCase):
    def setUp(self):
        self.mails = get_mail(1)
        get_one_sheet() 

    def test_overview_content_when_mail_id(self):
        """this function tests whether user can access mail/add.html with mail_id parameter"""
        all_mails = Mail.objects.all()
        given_id = all_mails[0].mail_id
        mail = self.mails[0]
        mail.resume = "test1"
        mail.plain_text = "test2 : Bonjour **M./Mme** **nom prop**"
        mail.save()
        response = self.client.get(reverse("mail:overview", kwargs={'mail_id':given_id}), follow=True)
        self.assertEqual(response.wsgi_request.get_full_path(), f"/spa/mail/overview/{given_id}/")
        self.assertContains(response, "test1")
        self.assertContains(response, "test2 : Bonjour Monsieur DUPONT")

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
        all_mails = Mail.objects.all()
        kwargs = { 'mail_id':all_mails[0].mail_id}
        response = self.client.get(reverse("mail:settings", kwargs=kwargs), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mail'].mail_id, kwargs['mail_id'])
        
    
    def test_post_data_received_ajax_1(self):
        """ this function tests whether mail.auto changes when received datas with: 
            {"ajax" : given_id}
        """
        all_mails = Mail.objects.all()
        given_id = all_mails[0].mail_id
        datas = {
            "ajax" : "1", 'mail_id':given_id, "auto_send" : "1"
        }
        before = Mail.objects.get(mail_id=given_id).auto_send
        print(before)
        response = self.client.post(reverse("mail:settings"), data=datas, follow=True)
        after = Mail.objects.get(mail_id=given_id).auto_send
        send_after_creation = Mail.objects.get(mail_id=given_id).send_after_creation
        print(after)
        self.assertTrue(before != after)
        self.assertTrue(send_after_creation)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"chgt" : "saved"})

    
    def test_post_form_is_valid(self): 
        """this function tests whether getattr(mail, given param]) change if I change the received datas
            according to what can be send by client
        """
        all_mails = Mail.objects.all()
        given_id = all_mails[0].mail_id
        self.mock_form.is_valid.return_value= True
        tab = ['send_after_creation', 'send_after_modif', 'send_after_delete', \
        'send_every_2_weeks', 'send_when_neuterable']
        for number in range(len(tab)):
            res = str(number+1)
            datas = {"frequency" : res}
            print("-----------------------------------------------")
            print("data : ", datas, number)
            mail = Mail.objects.get(mail_id=given_id)
            before = getattr(mail, tab[number])
            print(f"\tauto save : {mail.auto_send} | {tab[number]} : {getattr(mail, tab[number])}")
            response = self.client.post(reverse("mail:settings", kwargs={'mail_id':given_id}), 
                data=datas, follow=True)
            mail = Mail.objects.get(mail_id=given_id)
            after = getattr(mail, tab[number])
            print(f"\tauto save : {mail.auto_send} | {tab[number]} : {getattr(mail, tab[number])}")
            self.assertTrue(response.status_code, 200)
            self.assertTrue(before != after)
            print("fin")



