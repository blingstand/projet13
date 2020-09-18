#python 
from datetime import datetime
from unittest import mock,skip
from datetime import datetime

#from django
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

#from apps
from .utils import Utils #get_animals_for_template, get_animal_from_given_id
from .models import Animal, Owner, AdminData
from .form import SheetForm
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
            mail = f'my{str(n)}@mail.com',
            caution = '0e')
        owner.save()
        animal = Animal(
            name = f"a{str(n)}",
            date_of_birth = datetime(2020,1,2).date(),
            race = 'bâtard',
            species = 0,
            color = 'grey',
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
        mail = 'my2@mail.com',
        caution = '0e',)
    owner.save()

class UnitTest(TestCase):
    def setUp(self):
        self.admin = AdminData(
            file="123",
            is_neutered = 0)
        self.admin.save()
        self.owner = Owner(
            owner_name = 'name',
            owner_surname = 'surname',
            owner_sex = 0,
            phone = '1234567890',
            mail = 'my@mail.com',
            caution = '0e',)
        self.owner.save()
        self.animal = Animal(
            name = "a",
            date_of_birth = datetime(2020,1,2).date(),
            race = 'bâtard',
            species = 0,
            color = 'grey',
            date_of_adoption = datetime(2020,9,18).date())
        self.animal.save()
        self.animal.admin_data = self.admin
        self.animal.owner = self.owner
        self.animal.save()
        self.utils = Utils()
        self.request_post = { 
        'name': 'a', 'date_of_birth': '02/01/2020', 'date_of_adoption': '18/09/2020', 
        'date_of_neuter': '', 'species': '0', 'is_neutered': '1', 'futur_date_of_neuter': '', 
        'race': 'bâtard', 'color': 'grey', 'observation': 'ronronne bruyamment', 
        'file': 'sus123', 'tatoo': '', 'chip': '', 'caution': '0e', 'mail_reminder': '0', 
        'tel_reminder': '0', 'owner_name': 'name', 'owner_surname': 'surname', 'owner_sex': '0',
        'phone': '1234567890', 'mail': 'my@mail.com', 'status': ''}
        self.request_post2 = { 
        'name': 'a', 'date_of_birth': '02/01/2020', 'date_of_adoption': '18/09/2020', 
        'date_of_neuter': '', 'species': '0', 'is_neutered': '1', 'futur_date_of_neuter': '', 
        'race': 'bâtard', 'color': 'grey', 'observation': 'ronronne bruyamment', 
        'file': 'sus123', 'tatoo': '', 'chip': '', 'caution': '0e', 'mail_reminder': '0', 
        'tel_reminder': '0', 'owner_name': 'name2', 'owner_surname': 'surname2', 'owner_sex': '0',
        'phone': '1122334455', 'mail': 'mySecond@mail.com', 'status': ''}
    skip    
    def test_get_animal_for_template(self):
        ''' tests if the function returns a list of animal objects '''
        list_animals = self.utils.get_animals_for_template()
        self.assertEqual(list_animals[0], self.animal)
    skip
    def test_get_animal_from_given_id(self):
        ''' tests if the function returns a list of animal objects using a given id '''
        list_animals = self.utils.get_animal_from_given_id(1)
        self.assertEqual(list_animals[0], self.animal)

    def test_change_date_format(self):
        """ this function tests if the format is changed when dict_values[data] is str or empty"""
        dict_values = {}
        keys = ('date_of_birth', 'date_of_adoption', 'date_of_neuter', 'futur_date_of_neuter')
        values = ("22/02/1991", "05/05/1988", "", "")
        for i in range(0, 4):
            dict_values[keys[i]] = values[i]
        result = self.utils.change_date_format(dict_values)
        
        self.assertTrue(result['date_of_birth'] == datetime(1991,2,22).date())
        self.assertTrue(result['date_of_neuter'] == None)
    
    def test_find_changes(self):
        """this function tests if find_change can detect 6 changes among these datas
        """
        given_id = Animal.objects.get(name="a").animal_id
        result = self.utils.find_changes(given_id,self.request_post)
        # print(len(result), result)
        self.assertTrue(len(result) == 6)
    
    def test_modify_datas_case_1(self):
        """this function test data modification in db when case 1 occures"""
        animal = Animal.objects.get(name="a")
        given_id = animal.animal_id
        create_new_owner()
        self.request_post['former_owner'] = "2"
        self.request_post['phone'] = '1234567891'
        self.request_post['mail'] = 'my@mail2.com'
        result = self.utils.modify_datas(given_id, self.request_post)
        # self.assertTrue(animal.owner.id == 2)
        self.assertTrue(result[0])
        self.assertTrue(Animal.objects.get(name="a").owner.id == 2)

    def test_modify_datas_case_2(self):
        """this function test data modification in db when case 2 occures"""
        animal = Animal.objects.get(name="a")
        given_id = animal.animal_id
        self.request_post2['former_owner'] = "0"
        result = self.utils.modify_datas(given_id, self.request_post2)
        # self.assertTrue(animal.owner.id == 2)
        self.assertTrue(result[0])
        self.assertTrue(Animal.objects.get(name="a").owner.id == 2)

    def test_modify_datas_case_3(self):
        """this function test data modification in db when case 3 occures"""
        animal = Animal.objects.get(name="a")
        given_id = animal.animal_id
        self.request_post['former_owner'] = "1"
        result = self.utils.modify_datas(given_id, self.request_post)
        self.assertTrue(result[0])
        self.assertTrue(Animal.objects.get(name="a").owner.id == 1)

class TestSheetForm(TestCase):  
    """ tests the methods from the class form SheetForm """
    def setUp(self):

        self.sf = SheetForm()
        self.sf.cleaned_data = {'caution': '0e', 'chip': '', 'date_of_adoption': datetime(2015, 6, 20).date(), \
        'date_of_birth': datetime(2015, 2, 15).date(), 'date_of_neuter': datetime(2015, 6, 22).date(), \
        'futur_date_of_neuter': None, 'file': 'g22h687', 'is_neutered': 1, \
        'mail': 'micro2@gmail.com', 'mail_reminder': 0, 'name': 'gims78', 'status': 'gims chante', \
        'owner_name': 'Miley', 'owner_surname': 'Krofon', 'owner_sex': 0, 'observation': 'porte des lunettes', \
        'color': 'noir', 'race': 'gros batard', 'species': 1, 'tatoo': '777', 'phone': '0302010607', 'tel_reminder': 0}
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
        output2 = self.sf.save_new_datas(self.dict_values)
        animal2 = Animal.objects.all()
        self.assertTrue('Erreur' in output2)
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
        get_many_entries(3)
        self.u = Utils()

    def test_get_access_page(self):
        """tests if user can access index.html from url"""
        response = self.client.get(reverse("sheet:index"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_access_datas(self):
        """tests if server can access POST data from index.html"""
        response = self.client.post(reverse("sheet:index"), data={"checkbox":['1']}) #data = returned data from form
        self.assertRedirects(response, reverse("sheet:index"))

    def test_drop_1_data_unique_owner(self):
        before = len(Animal.objects.all())
        self.u.drop_sheet((1,))
        after = len(Animal.objects.all())

        self.assertTrue(before == after + 1)

    def test_drop_1_data_not_unique_owner(self):
        """test if 1 animalsheet will be droped and owner remain 
        in base because he is not unique""" 
        a1, a2 = Animal.objects.all()[0:2]
        same_owner = a1.owner

        a2.owner = same_owner
        a2.save()
        self.assertTrue(a1.owner == a2.owner) #they have same owner
        before_a = len(Animal.objects.all())
        before = len(Owner.objects.all())
        self.u.drop_sheet((a1.animal_id, ))
        after_a = len(Animal.objects.all())
        after = len(Owner.objects.all())

        self.assertTrue(before == after)
        self.assertTrue(before_a == after_a + 1)

    def test_drop_many_data_unique_owner(self):
        before = len(Animal.objects.all())
        self.u.drop_sheet((1,2,3))
        after = len(Animal.objects.all())
        print("before", before)
        print("after", after)
        self.assertTrue(before == after + 3)

class TestAddSheetViews(TestCase):

    def setUp(self):
        get_one_entry()
        patcher = mock.patch("sheet.views.SheetForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value

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
        response = self.client.post(reverse("sheet:add"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_js_response(self):
        """ tests the given context when post receives ajax request like : 
                datas = {
                    'ask_owner_data':"1", "owner_id":1}
        """
        datas = {
                    'ask_owner_data':"1", "owner_id":1
                }
        selected_owner = Owner.objects.get(id=1)
        expected_datas = {
            'mail': selected_owner.mail, 
            'name': selected_owner.owner_name,
            'phone': selected_owner.phone, 
            'sex': selected_owner.owner_sex,
            'surname': selected_owner.owner_surname,
        }
        print(selected_owner.owner_name)
        print(selected_owner.owner_surname)
        response = self.client.post(reverse("sheet:add"), data=datas, follow=True)

        self.assertJSONEqual(str(response.content, encoding='utf8'), {'data': expected_datas})

class TestAlterSheetViews(TestCase): 

    def setUp(self):
        self.animal, self.admin, self.owner = get_one_entry()
    def test_get_access_page(self):
        """ tests if user can access get page """
        response = self.client.get(reverse("sheet:alter", kwargs={'given_id':1}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.name)