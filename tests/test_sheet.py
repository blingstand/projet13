#python 
from datetime import datetime
from unittest import mock,skip
from datetime import datetime

#from django
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

#from apps
from sheet.utils import UtilsSheet #get_animals_for_template, get_animal_from_given_id
from sheet.models import Animal, Owner, AdminData, Contact
from sheet.form import SheetForm
#-- unit test --
def get_one_entry():
    """ create one sheet in db and return """
    admin = AdminData(
        is_neutered = 0, 
        file='123') #charfield
    admin.save()
    owner = Owner(
        owner_name = 'name',
        owner_surname = 'surname',
        owner_sex = 0,
        phone = '1234567890',
        mail = 'my@mail.com')
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

def get_many_entries(number): 
    for n in range(1, number + 1):
        admin = AdminData(
            is_neutered = 0, 
            file='123'+str(n))
        admin.save()
        owner = Owner(
            owner_name = 'name'+str(n), 
            owner_surname = 'surname',
            owner_sex = 0,
            phone = '123456789'+str(n),
            mail = f'my{str(n)}@mail.com')
        owner.save()
        animal = Animal(
            name = f"a{str(n)}",
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

def create_new_owner():
    owner = Owner(
        owner_name = 'name2',
        owner_surname = 'surname2',
        owner_sex = 0,
        phone = '1234567891',
        mail = 'my2@mail.com')
    owner.save()

def create_contact(qtt): 
    """ this function creates a new contact """
    owner = Owner.objects.all()[0]
    for elem in range(qtt): 
        new_contact = Contact(
            contact_date = "2020-10-16",
            resume = f"resume n°{elem}",
            full_text = f"full_text n°{elem}",
            nature = "0",
            owner = owner)
        new_contact.save()

class RedirectView(TestCase):
    def test_redirect_index(self):
        """this function test whether the user is redirected when end url is empty"""
        response = self.client.get("", follow=True)
        self.assertEqual(response.status_code, 200)   

class UnitTest(TestCase):
    def setUp(self):
        self.u = UtilsSheet()
        self.admin = AdminData(
            file="123",
            is_neutered = 0)
        self.admin.save()
        self.owner = Owner(
            owner_name = 'name',
            owner_surname = 'surname',
            owner_sex = 0,
            phone = '1234567890',
            mail = 'my@mail.com',)
        self.owner.save()
        self.animal = Animal(
            name = "A",
            date_of_birth = datetime(2020,1,2).date(),
            race = 'bâtard',
            species = 0,
            color = 'grey',
            caution = '0',
            date_of_adoption = datetime(2020,9,18).date())
        self.animal.save()
        self.animal.admin_data = self.admin
        self.animal.owner = self.owner
        self.animal.save()
        self.utils = UtilsSheet()
        self.request_post = {'caution': '100', 'chip': '556231945165215', 'color': 'a', 
        'date_of_adoption': '2020-10-11', 'date_of_birth': '2020-10-11', 
        'date_of_neuter': 'None', 'futur_date_of_neuter': 'None', 'file': '', 
        'is_neutered': '0', 'select_owner': 25, 'mail': 'my@mail.com', 
        'name': 'A', 'nature_caution': '0', 'status': '', 'owner_name': 'name', 
        'owner_surname': 'surname', 'owner_sex': '0', 'phone': '1234567890',
         'race': 'a', 'species': '0', 'tatoo': ''}

        self.request_post2 = {'caution': '100', 'chip': '556231945165215', 'color': 'a', 
        'date_of_adoption': '2020-10-11', 'date_of_birth': '2020-10-11', 
        'date_of_neuter': 'None', 'futur_date_of_neuter': 'None', 'file': '', 
        'is_neutered': '0', 'select_owner': 25, 'mail': 'my2@mail.com', 
        'name': 'A', 'nature_caution': '0', 'status': '', 'owner_name': 'name2', 
        'owner_surname': 'surname2', 'owner_sex': '0', 'phone': '1234567891',
         'race': 'a', 'species': '0', 'tatoo': ''}

        self.dict_values = {
            "owner_name" : "chopin",
            "owner_surname" : "fred",
            "owner_sex" : "0",
            "phone" : "0623129859",
            "mail" : "chopmal@mail.fr",
        }

    
    def test_get_animal_from_given_id(self):
        ''' tests if the function returns a list of animal objects using a given id '''
        
        list_animals = self.utils.get_animal_from_given_id(self.animal.id)
        self.assertEqual(list_animals[0], self.animal)
    
    def test_change_date_format(self):
        """ this function tests if the format is changed when dict_values[data] is str or empty"""
        dict_values = {}
        keys = ('date_of_birth', 'date_of_adoption', 'date_of_neuter', 'futur_date_of_neuter')
        values = ("1991-02-22", "1998-05-05", "", "")
        for i in range(0, 4):
            dict_values[keys[i]] = values[i]
        result = self.utils.change_date_format(dict_values)
        
        self.assertTrue(result['date_of_birth'] == datetime(1991,2,22).date())
        self.assertTrue(result['date_of_neuter'] == None)
        
    def test_find_changes(self):
        """this function tests if find_change can detect 6 changes among these datas
        """
        given_id = Animal.objects.get(name="A").id
        result = self.utils.find_changes(given_id, self.request_post)
        print('*********debug ')
        # print(len(result), result)
        self.assertTrue(len(result) == 10)
        
    def test_manage_modify_datas_case_1(self):
        """this function test data modification in db when case 1 occures"""
        animal = Animal.objects.get(name="A")
        given_id = animal.id
        create_new_owner()
        owner2_id = Owner.objects.get(owner_name="name2").id
        self.request_post['select_owner'] = owner2_id
        self.request_post['phone'] = '1234567891'
        self.request_post['mail'] = 'my@mail2.com'
        result = self.utils.manage_modify_datas(given_id, self.request_post)
        # self.assertTrue(animal.owner.id == 2)
        self.assertTrue(result[0])
        self.assertTrue(Animal.objects.get(name="A").owner.id == owner2_id)
    
    def test_manage_modify_datas_case_2(self):
        """this function test data modification in db when case 2 occures"""
        print("test_manage_modify_datas_case_2")
        print("********")

        animal = Animal.objects.get(name="A")
        given_id = animal.id
        owner_id = animal.owner.id
        self.request_post2['select_owner'] = "0"
        result = self.utils.manage_modify_datas(given_id, self.request_post2)
        # self.assertTrue(animal.owner.id == 2)
        self.assertTrue(result[0])
        print("1/ ", Animal.objects.get(name="A").owner.id)
        print("2/ ", owner_id)
        print("***************")
        self.assertTrue(Animal.objects.get(name="A").owner.id == owner_id + 1 )
    
    def test_manage_modify_datas_case_3(self):
        """this function test data modification in db when case 3 occures"""
        animal = Animal.objects.get(name="A")
        given_id = animal.id
        owner_id = animal.owner.id
        self.request_post['select_owner'] = owner_id
        result = self.utils.manage_modify_datas(given_id, self.request_post)
        self.assertTrue(result[0])
        self.assertTrue(Animal.objects.get(name="A").owner.id == owner_id)

    
    def test_drop_1_data_unique_owner(self):
        before = len(Animal.objects.all())
        self.utils.drop_sheet((Animal.objects.all()[0].id,))
        after = len(Animal.objects.all())

        self.assertTrue(before == after + 1)
    
    def test_drop_1_data_not_unique_owner(self):
        """test if 1 animalsheet will be droped and owner remain 
        in base because he is not unique""" 
        print("test - same owner ")
        get_many_entries(2)
        a1, a2 = Animal.objects.all()[0:2]
        same_owner = a1.owner
        a2.owner = same_owner
        a2.save()
        self.assertTrue(a1.owner == a2.owner) #they have same owner
        before_a = len(Animal.objects.all())
        before = len(Owner.objects.all())
        self.utils.drop_sheet((a1.id, ))
        after_a = len(Animal.objects.all())
        after = len(Owner.objects.all())

        self.assertTrue(before == after)
        self.assertTrue(before_a == after_a + 1)
    
    def test_drop_many_data_unique_owner(self):
        """ tests if sheets will be drop when anim belong to same owner """
        print("test - diff owner ")
        get_many_entries(3)
        a1, a2, a3 = Animal.objects.all()[0:3]
        before = len(Animal.objects.all())
        self.utils.drop_sheet((a1.id, a2.id, a3.id))
        after = len(Animal.objects.all())
        print("\n\n")
        print("test_drop_many_data_unique_owner before", before)
        print("test_drop_many_data_unique_owner after", after)
        self.assertTrue(before == after + 3)
    
    def test_check_owner_values(self):
        """test if this function can handles integrity pb : same phone number/same mail"""
        print("test_check_owner_values")
        print(Owner.objects.all()[0].phone)
        print(Owner.objects.all()[0].mail)
        dict_value1 = {'phone' : Owner.objects.all()[0].phone, 'mail' :"test@mail.fr"} 
        dict_value2 = {'phone' : "0632313232", 'mail' : Owner.objects.all()[0].mail} 
        ow_id = Owner.objects.all()[0].id
        resp1 = self.utils.check_owner_values(dict_value1)
        resp2 = self.utils.check_owner_values(dict_value2)
        resp3 = self.utils.check_owner_values(dict_value1, ow_id, True)
        resp4 = self.utils.check_owner_values(dict_value2, ow_id, True)
        get_many_entries(1)
        another_owner = Owner.objects.get(id=ow_id+1)
        resp5 = self.utils.check_owner_values(dict_value1, another_owner.id, True)
        resp6 = self.utils.check_owner_values(dict_value2, another_owner.id, True)
        
        self.assertEqual(resp1[0], False) #not a modif same value > false
        self.assertEqual(resp2[0], False)
        self.assertEqual(resp3[0], True) #is modif same value for same owner > true 
        self.assertEqual(resp4[0], True)
        self.assertEqual(resp5[0], False) #is modif same value diff owner > false
        self.assertEqual(resp6[0], False)
    
    def test_create_owner_with_no_return(self):
        """tests the return of create_owner function"""
        
        resp = self.utils.create_owner(self.dict_values)
        self.assertEqual(resp[0], True) #it works

        self.dict_values['mail'] = 19566
        resp2 = self.utils.create_owner(self.dict_values)
        self.assertEqual(resp2[0], False) #it does not works

        dict_values = {
            "owner_name" : "chopin"
            }
        resp3 = self.utils.create_owner(dict_values)
        self.assertEqual(resp3[0], False) #it raises error
    
    def test_modify_owner(self):
        """tests if you can mosify an owner with given id and dict_values"""
        ow_id = Owner.objects.all()[0].id
        resp = self.utils.modify_owner(ow_id, self.dict_values)
        self.assertEqual(resp[0], True)

        get_many_entries(1)
        another_owner = Owner.objects.get(id=ow_id+1)
        resp2 = self.utils.modify_owner(another_owner.id, self.dict_values)
        self.assertEqual(resp2[0], False) #it does not works

        dict_values = {
            "owner_name" : "chopin"
            }
        resp3 = self.utils.modify_owner(ow_id, dict_values)
        self.assertEqual(resp3[0], False) #it raises error

    def test_remove_contact(self):
        """test if contacts are delete if a list of ids is given"""
        create_contact(5)
        before = len(Contact.objects.all())
        list_id_contact = [contact.id for contact in Contact.objects.all()]
        list_id_contact = list_id_contact[0:3]
        resp = self.utils.remove_contact(list_id_contact)
        after = len(Contact.objects.all())
        self.assertTrue(resp[0])
        self.assertEqual(before, after + 3)
        resp_error = self.utils.remove_contact("error")
        self.assertFalse(resp_error[0])

    def test_modify_contact(self):
        """test if contacts are modified when a list of ids and 
        new datas are given"""
        create_contact(1)
        dict_values = {}
        dict_values['id_modif'] = Contact.objects.all()[0].id
        dict_values['resume'] = "new resume for test"
        resp = self.utils.modify_contact(dict_values)
        self.assertTrue(resp[0])

        dict_values['nature'] = "error for test"
        resp = self.utils.modify_contact(dict_values)
        self.assertFalse(resp[0])
        
    def test_remove_owner_adapt_not_list_id(self):
        """tests if remove_owner can remove owner if a single id is given"""
        create_new_owner()
        print([owner.id for owner in Owner.objects.all().order_by("-id")])
        given_id = Owner.objects.all().order_by("-id")[0].id
        resp = self.utils.remove_owner(given_id)
        self.assertTrue(resp[0])

        given_id = Owner.objects.all().order_by("id")[0].id
        resp = self.utils.remove_owner(given_id)
        self.assertFalse(resp[0])

class TestSheetForm(TestCase):  
    """ tests the methods from the class form SheetForm """
    def setUp(self):
        create_new_owner()
        given_id = Owner.objects.all()[0].id
        self.sf = SheetForm()
        self.sf.cleaned_data = {'caution': '100', 'chip': '556231945165215', 'color': 'a', 
        'date_of_adoption': '2020-10-11', 'date_of_birth': '2020-10-11', 
        'date_of_neuter': 'None', 'futur_date_of_neuter': 'None', 'file': '', 
        'is_neutered': '0', 'select_owner': given_id, 'mail': 'my@mail.com', 
        'name': 'A', 'nature_caution': '0', 'status': '', 'owner_name': 'name', 
        'owner_surname': 'surname', 'owner_sex': '0', 'phone': '1234567890',
         'race': 'a', 'species': '0', 'tatoo': ''}
        self.dict_values = self.sf.from_form()


    def test_from_form(self):
        """ test if the function returns a dictionary of values to fill rows in tables,
        then test the key of each list_values"""
        dict_to_test = self.sf.from_form()
        list_keys = []
        for key in dict_to_test:
            list_keys.append(key)
        self.assertTrue(isinstance(dict_to_test, dict))
        self.assertEqual(['animal', 'admin', 'owner'], list_keys)

    def test_save_new_datas(self):
        """ tests if the function can save given classes in the db"""
        all_entries = Animal.objects.all()
        nb_entries = len(all_entries)
        output = self.sf.save_new_datas(self.dict_values)
        all_entries2 = Animal.objects.all()
        nb_entries2 = len(all_entries2)
        self.assertTrue(nb_entries < nb_entries2)
    
    
    def test_2nd_same_sheet_added(self): 
        """ test if the base will not be changed when 2nd same sheet tries to be add"""
        output = self.sf.save_new_datas(self.dict_values)
        animal = Animal.objects.all()
        self.dict_values["chip"]="556231945165222"
        output2 = self.sf.save_new_datas(self.dict_values)
        animal2 = Animal.objects.all()
        self.assertTrue('Erreur' in output2[0])
        self.assertTrue(len(animal) == len(animal2))

    def test_accept_2nd_animal_same_owner_added(self): 
        """ tests if 2nd sheet entries will be added if 2 diff animals have the same user """
        output = self.sf.save_new_datas(self.dict_values)
        #2nd animal
        self.sf.cleaned_data['name'] = 'gims'
        self.sf.cleaned_data['file'] = 'gims123'
        self.dict_values = self.sf.from_form()
        output2 = self.sf.save_new_datas(self.dict_values)
        all_entries = len(Animal.objects.all())
        self.assertTrue(all_entries == 2)

    def test_reject_2nd_animal_same_file(self):
        """ tests if second animal will not been accepted if his file number already exist """
        output = self.sf.save_new_datas(self.dict_values)
        first_animal = Animal.objects.all()[0]
        first_admin, first_owner = first_animal.admin_data, first_animal.owner
        #2nd animal
        self.sf.cleaned_data['name'] = 'gims'
        self.dict_values = self.sf.from_form()
        output2 = self.sf.save_new_datas(self.dict_values)
        all_entries = len(Animal.objects.all())
        self.assertTrue(all_entries == 1)
        self.assertTrue(Animal.objects.all()[0] == first_animal)
        self.assertTrue(AdminData.objects.all()[0] == first_admin)
        self.assertTrue(Owner.objects.all()[0] == first_owner)

class TestSheetViews(TestCase):
    """ test the class SheetViews for index.html """
    def setUp(self):
        self.animal, self.admin, self.owner = get_one_entry()
        self.u = UtilsSheet()
        patcherGradat = mock.patch("mydashboard.utils.GraphDatas")
        self.addCleanup(patcherGradat.stop) #called after teardown
        mock_gradat_class = patcherGradat.start()
        self.mock_gradat = mock_gradat_class.return_value
        

    
    def test_get_access_page(self):
        """tests if user can access index.html from url"""
        response = self.client.get(reverse("sheet:index"), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_post_own0(self):
        """tests if server can access POST data from index.html"""
        kwargs = {"own":0}
        anim_id = Animal.objects.all()[0].id
        response = self.client.post(reverse("sheet:index", kwargs=kwargs),  data={"checkbox":anim_id}, follow=True) 
        #data = returned data from form
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("sheet:index", kwargs={'own':0}))
    
    def test_post_own1(self):
        """tests if server can access POST data from index.html"""
        kwargs = {"own":1}
        owner_id = Owner.objects.all()[0].id
        response = self.client.post(reverse("sheet:index", kwargs=kwargs),  data={"checkbox":owner_id}, follow=True) 
        #data = returned data from form
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("sheet:index", kwargs={'own':1}))
    
    # def test_get_act_display_search_1(self): 
    #     """tests get return when 
    #         action = 'display', search = "1" 
    #     """
    #     get_many_entries(4)
    #     list_owners= [owner for owner in Owner.objects.all()]
    #     list_contacted = list_owners[0:2]
    #     list_to_contact = list_owners[2:]
    #     self.mock_gradat.get_list_for_search.new_callable=mock.PropertyMock
    #     self.mock_gradat.get_list_for_search = list_owners, list_contacted, list_to_contact
    #     print('test_get_act_display_search_1', self.mock_gradat.get_list_for_search)
    #     kwargs = {"action":"display", "search":1, 'own':1}
    #     response = self.client.get(reverse("sheet:index", kwargs=kwargs),  follow=True) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.wsgi_request.get_full_path(),  "/spa/sheet/index/1/display/1")
    #     self.assertEqual(len(response.context["owners"]), len(list_owners))

    
    # def test_get_act_display_search_2(self): 
    #     """tests get return when 
    #         action = 'display', search = "1" 
    #     """
    #     get_many_entries(4)
    #     list_owners= [owner for owner in Owner.objects.all()]
    #     list_contacted = list_owners[0:2]
    #     list_to_contact = list_owners[2:]
    #     self.mock_gradat.get_list_for_search.return_value = list_owners, list_contacted, list_to_contact
    #     kwargs = {"action":"display", "search":2, 'own':1}
    #     response = self.client.get(reverse("sheet:index", kwargs=kwargs),  follow=True) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.wsgi_request.get_full_path(),  "/spa/sheet/index/1/display/2")
    #     self.assertEqual(len(response.context["owners"]), len(list_contacted))
    
    # def test_get_act_display_search_3(self): 
    #     """tests get return when 
    #         action = 'display', search = "1" 
    #     """
    #     get_many_entries(4)
    #     list_owners= [owner for owner in Owner.objects.all()]
    #     list_contacted = list_owners[0:2]
    #     list_to_contact = list_owners[2:]
    #     self.mock_gradat.get_list_for_search.new_callable=mock.PropertyMock
    #     self.mock_gradat.get_list_for_search = list_owners, list_contacted, list_to_contact
    #     kwargs = {"action":"display", "search":3, 'own':1}
    #     response = self.client.get(reverse("sheet:index", kwargs=kwargs),  follow=True) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.wsgi_request.get_full_path(), "/spa/sheet/index/1/display/3")
    #     self.assertEqual(len(response.context["owners"]), len(list_to_contact))


    # def test_get_action_prop(self):
    #     """tests get return when 
    #         action = 'display', search = "1" 
    #     """
    #     get_many_entries(4)
    #     first_owner = Owner.objects.all()[0]
    #     print(first_owner)
    #     kwargs = {"action":"search:prop",'own':1, 'search':first_owner.id}
    #     response = self.client.get(reverse("sheet:index", kwargs=kwargs),  follow=True) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.wsgi_request.get_full_path(), "/spa/sheet/index/1/search:prop/6")
    #     self.assertEqual(len(response.context["owners"]), 1)
    #     self.assertEqual(response.context["owners"][0].owner_name,\
    #      first_owner.owner_name)

    # def test_get_action_anim(self):
    #     """tests get return when 
    #         action = 'display', search = "1" 
    #     """
    #     get_many_entries(4)
    #     first_anim = Animal.objects.all()[0]
    #     print(first_anim)
    #     kwargs = {"action":"search:anim",'own':1, 'search':first_anim.id}
    #     response = self.client.get(reverse("sheet:index", kwargs=kwargs),  follow=True) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.wsgi_request.get_full_path(), f"/spa/sheet/index/1/search:anim/1")
    #     self.assertEqual(len(response.context["animals"]), 1)
    #     self.assertEqual(response.context["animals"][0].name,\
    #      first_anim.name)

class TestAddSheetViews(TestCase):

    def setUp(self):
        get_one_entry()
        patcher = mock.patch("sheet.views.SheetForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value
        given_id = Owner.objects.all()[0].id
        self.sf = SheetForm()
        self.mock_form.cleaned_data = {'caution': '100', 'chip': '556231945165215', 'color': 'a', 
        'date_of_adoption': '2020-10-11', 'date_of_birth': '2020-10-11', 
        'date_of_neuter': 'None', 'futur_date_of_neuter': 'None', 'file': '', 
        'is_neutered': '0', 'select_owner': given_id, 'mail': 'my@mail.com', 
        'name': 'A', 'nature_caution': '0', 'status': '', 'owner_name': 'name', 
        'owner_surname': 'surname', 'owner_sex': '0', 'phone': '1234567890',
         'race': 'a', 'species': '0', 'tatoo': ''}
        self.dict_values = self.mock_form.from_form()
    
    def test_get_access_page(self):
        """tests if user can access page from url"""
        response = self.client.get(reverse("sheet:add"), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_post_form_not_valid_error_msg(self):
        """ tests if the page is displayed with error message when form is not valid """
        self.mock_form.is_valid.return_value = False
        response = self.client.post(reverse("sheet:add"), follow=True)
        is_error = response.context["errors"]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_error)
    
    def test_post_form_is_valid(self):
        """ tests if the page is displayed with error message when form is not valid """
        self.mock_form.is_valid.return_value = True
        self.mock_form.save_new_datas.return_value = 1, Animal.objects.all()[0]
        response = self.client.post(reverse("sheet:add"), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_post_form_is_valid_but_issue(self):
        """ tests if the page is displayed with error message when form is not valid """
        self.mock_form.is_valid.return_value = True
        self.mock_form.save_new_datas.return_value = 0, "erreur créée par un mock"
        response = self.client.post(reverse("sheet:add"), follow=True)
        self.assertEqual(response.wsgi_request.get_full_path(), '/spa/sheet/index/add')
        self.assertEqual(response.status_code, 200)

class TestAlterSheetViews(TestCase): 

    def setUp(self):
        self.animal, self.admin, self.owner = get_one_entry()
        patcher = mock.patch("sheet.views.SheetForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value
        self.dict_values = {'caution': '0', 'chip': '', 'color': 'black', 
        'date_of_adoption': '2020-10-16', 'date_of_birth': '2020-01-02', 
        'date_of_neuter': '', 'futur_date_of_neuter': '', 
        'file': '123', 'is_neutered': '0', 'select_owner': self.owner.id, 
        'mail': 'my@mail.com', 'name': 'a', 'nature_caution': 'chèque', 
        'status': '', 'owner_name': 'name', 'owner_surname': 'newman', #surname became newman
         'owner_sex': '0', 'phone': '1234567890', 'race': 'bâtard', 
         'species': '0', 'tatoo': ''}
        #--

    def test_get_access_page(self):
        """ tests if user can access get page """

        response = self.client.get(reverse("sheet:alter",\
         kwargs={'given_id':self.animal.id}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.name)

    def test_post_valid(self):
        """ tests return if form is valid """
        self.mock_form.is_valid.return_value = True
        response = self.client.post(reverse("sheet:alter", \
            kwargs={'given_id':self.animal.id}), data=self.dict_values, follow=True)
        animal = Animal.objects.get(name="a")
        self.assertEqual(animal.color, "black")

    def test_post_not_valid(self):
        """ tests return if form is not valid """
        self.mock_form.is_valid.return_value = False
        response = self.client.post(reverse("sheet:alter", \
            kwargs={'given_id':self.animal.id}), data=self.dict_values, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.get_full_path(), f"/spa/sheet/index/alter/{self.animal.id}")

class TestAlterOwnerSheetView(TestCase): 

    def setUp(self):
        self.animal, self.admin, self.owner = get_one_entry()
        patcher = mock.patch("sheet.views.SheetForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value
    def test_get_access_page(self):
        """this function tests whether server can answer a get request when receiving an url and given_id param"""
        response = self.client.get(reverse("sheet:alter_owner", kwargs={'given_id':self.owner.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_action_delete(self):
        """ tests return if form is valid """
        before = Owner.objects.all()
        print(len(before))
        response = self.client.post(
            reverse("sheet:alter_owner", 
            kwargs={'given_id':self.owner.id, 'action':'delete'}), 
            follow=True)
        after = Owner.objects.all()
        print(len(after))
        self.assertContains(response, "pas été effacé(e)")

        create_new_owner()
        new_owner = Owner.objects.all().order_by('-id')[0]
        print("new owner ?", self.owner.id != new_owner.id)
        response = self.client.post(
            reverse("sheet:alter_owner", 
            kwargs={'given_id':new_owner.id, 'action':'delete'}), 
            follow=True)
        self.assertEqual(response.wsgi_request.get_full_path(), "/spa/sheet/index/1")


    def test_post_action_modify(self):
        """ tests return if form is valid """
        dict_values = { 
            "csrfmiddlewaretoken": "123",
            "owner_name" :  "name2", 
            "owner_surname" :  "surname2", 
            "owner_sex": "0", 
            "mail": "mailnum2@mail.fr", 
            "phone": "0554882221", 
        } 
        response = self.client.post(reverse("sheet:alter_owner", \
            kwargs={'given_id':self.owner.id, 'action':'modify'}), data=dict_values, follow=True) 
        owner = Owner.objects.get(id=self.owner.id)
        self.assertEqual(owner.owner_name, "Name2")

    def test_post_action_modify_but_error(self):
        """ tests return if form is valid but there is an error """
        dict_values = {"csrfmiddlewaretoken": "123"} 
        response = self.client.post(reverse("sheet:alter_owner", \
            kwargs={'given_id':self.owner.id, 'action':'modify'}), data=dict_values, follow=True) 
        owner = Owner.objects.get(id=self.owner.id)
        self.assertEqual(response.wsgi_request.get_full_path(), \
            f"/spa/sheet/index/alter_owner/{self.owner.id}/modify")


class TestAddOwnerSheetView(TestCase):

    def setUp(self):
        self.animal, self.admin, self.owner = get_one_entry()
        patcher = mock.patch("sheet.views.SheetForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value

    def test_get(self):
        """ test get function """
        response = self.client.get(reverse("sheet:add_owner"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.get_full_path(), f"/spa/sheet/index/add_owner")

    def test_post_form_is_valid(self):
        """ test post function, if it creates an ower"""
        self.mock_form.is_valid.return_value = True
        dict_values = { 
            "csrfmiddlewaretoken": "123",
            "owner_name" :  "name2", 
            "owner_surname" :  "surname2", 
            "owner_sex": "0", 
            "mail": "mailnum2@mail.fr", 
            "phone": "0554882221", 
        } 
        response = self.client.post(
            reverse("sheet:add_owner"), data=dict_values, follow=True) 
        owner = Owner.objects.get(owner_name="Name2")
        self.assertTrue(owner.owner_name == 'Name2') 
        self.assertEqual(response.wsgi_request.get_full_path(), f"/spa/sheet/index/1")

    def test_post_form_is_not_valid(self):
        """ test post function, if it creates an ower"""
        self.mock_form.is_valid.return_value = True
        dict_values = { "csrfmiddlewaretoken": "123"} 
        response = self.client.post(reverse("sheet:add_owner"), data=dict_values, follow=True) 
        self.assertEqual(response.wsgi_request.get_full_path(), "/spa/sheet/index/add_owner")

class TestModelsSheet(TestCase):
    """class with tests for models methods and properties"""
    
    def setUp(self):
        """charged before each test"""
        pass


    def test_str_animal(self):
        """tests if returned string for class is like expected"""
        get_one_entry()
        anim = Animal.objects.all()[0]
        self.assertEqual("a (dossier : 123)", str(anim))
        new_admin = AdminData()
        new_admin.save()
        anim.admin_data = new_admin
        anim.save()
        self.assertEqual("a", str(anim))

    def test_str_species(self):
        """tests if the property return a str type"""
        get_one_entry()
        anim = Animal.objects.all()[0]
        self.assertTrue(isinstance(anim.str_species, str))

    def test_last_contact(self):
        """test if last_contact property can return what I expect"""
        get_one_entry()
        create_contact(1)
        owner = Owner.objects.all()[0]
        contact = Contact.objects.all()[0] 
        self.assertTrue(owner.last_contact == None)

        contact.nature = "3"
        contact.save()
        contact.owner = owner
        self.assertEqual(owner.last_contact.nature, contact.nature)

    def test_to_contact(self):
        """test if to_contact property can return what I expect"""
        get_one_entry()
        owner = Owner.objects.all()[0]
        self.assertEqual(owner.to_contact, None)
        create_contact(1)
        contact = Contact.objects.all()[0]
        owner.to_contact
        self.assertEqual(owner.to_contact, False)
        contact.contact_date = "2020-2-3"
        contact.save()
        self.assertEqual(owner.to_contact, True)

    def test_escaped_charac_text(self):
        """test if to_contact property can return what I expect"""
        get_one_entry()
        create_contact(1)
        owner = Owner.objects.all()[0]
        contact = Contact.objects.all()[0] 
        contact.full_text = "line1\\n\\nline2"
        print(contact.escaped_charac_text)
        self.assertEqual(contact.escaped_charac_text, 'line1\nline2')

    def test_reduced_text(self):
        """test if reduced_text property can return a len(100) text + 4 str"""
        get_one_entry()
        create_contact(1)
        owner = Owner.objects.all()[0]
        contact = Contact.objects.all()[0] 
        contact.full_text = "**"*100
        print(len(contact.escaped_charac_text))
        self.assertEqual(len(contact.reduced_text), 100+4)