#python 
from datetime import datetime
from unittest import mock, skip

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
        owner_sex = 'M',
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
            owner_sex = 'M',
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

class UnitTest(TestCase):
    def setUp(self):
        self.admin = AdminData(
            is_neutered = 0)
        self.admin.save()
        self.owner = Owner(
            owner_name = 'name',
            owner_surname = 'surname',
            owner_sex = 'M',
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
            date_of_adoption = datetime.now())
        self.animal.save()
        self.animal.admin_data = self.admin
        self.animal.owner = self.owner
        self.animal.save()
        self.utils = Utils()
        
    def test_get_animal_for_template(self):
        ''' tests if the function returns a list of animal objects '''
        list_animals = self.utils.get_animals_for_template()
        self.assertEqual(list_animals[0], self.animal)

    def test_get_animal_from_given_id(self):
        ''' tests if the function returns a list of animal objects using a given id '''
        list_animals = self.utils.get_animal_from_given_id(1)
        self.assertEqual(list_animals[0], self.animal)


class TestSheetForm(TestCase):  
    """ tests the methods from the class form SheetForm """
    def setUp(self):

        self.sf = SheetForm()
        self.sf.cleaned_data = {'caution': '0e', 'chip': '', 'date_of_adoption': datetime(2015, 6, 20).date(), \
        'date_of_birth': datetime(2015, 2, 15).date(), 'date_of_neuter': datetime(2015, 6, 22).date(), \
        'futur_date_of_neuter': None, 'file': 'g22h687', 'is_neutered': 1, \
        'mail': 'micro2@gmail.com', 'mail_reminder': 0, 'name': 'gims78', 'status': 'gims chante', \
        'owner_name': 'Miley', 'owner_surname': 'Krofon', 'owner_sex': 'H', 'observation': 'porte des lunettes', \
        'color': 'noir', 'race': 'gros batard', 'species': '1', 'tatoo': '777', 'phone': '0302010607', 'tel_reminder': 0}
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


    def test_modify_data_3changes_for_Animal(self):
        """ test if the db is different before and after a modification """
        #I had a new Sheet
        output = self.sf.save_new_datas(self.dict_values)
        first_animal = Animal.objects.all()[0]
        first_admin, first_owner = first_animal.admin_data, first_animal.owner
        former_name = first_animal.name
        #I get new data, different name with same admin and same owner
        #I need to alter db 
        self.sf.cleaned_data['name'] = 'gims'
        self.sf.cleaned_data['color'] = 'blue'
        self.sf.cleaned_data['observation'] = "c'est un maître chat"
        self.dict_values = self.sf.from_form()
        given_id = first_animal.animal_id
        output2 = self.sf.modify_datas(given_id)
        second_animal = Animal.objects.all()[0]
        self.assertTrue(first_animal.name == 'gims78')
        self.assertTrue(second_animal.name == 'gims')
        self.assertIn(output2[0:3], '> 3')

    def test_modify_data_changes_for_Admin_and_Owner(self):
        """ test if the db is different before and after a modification """
        #I had a new Sheet
        output = self.sf.save_new_datas(self.dict_values)
        first_animal = Animal.objects.all()[0]
        first_admin, first_owner = first_animal.admin_data, first_animal.owner
        #I get new data, different name with same admin and same owner
        #I need to alter db 
        self.sf.cleaned_data['owner_name'] = 'fabrice'
        self.sf.cleaned_data['is_neutered'] = 3
        self.sf.cleaned_data['futur_date_of_neuter'] = datetime(2020,1,12).date()
        self.dict_values = self.sf.from_form()
        given_id = first_animal.animal_id
        output2 = self.sf.modify_datas(given_id)
        second_animal = Animal.objects.all()[0]
        self.assertTrue(second_animal.owner.owner_name == 'fabrice')
        self.assertTrue(second_animal.admin_data.is_neutered == 3)
        self.assertTrue(second_animal.admin_data.futur_date_of_neuter == datetime(2020,1,12).date())
        self.assertIn(output2[0:3], '> 3')

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



class TestAlterSheetViews(TestCase): 

    def setUp(self):
        self.animal, self.admin, self.owner = get_one_entry()
    def test_get_access_page(self):
        """ tests if user can access get page """
        response = self.client.get(reverse("sheet:alter", kwargs={'given_id':1}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.name)