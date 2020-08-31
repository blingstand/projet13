#python 
from datetime import datetime
from unittest import mock, skip

#from django
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

#from apps
from .utils import get_animals_for_template, get_animal_from_given_id
from .models import Animal, Owner, AdminData
from .form import SheetForm
#-- unit test --
@skip
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
            species = 'chat',
            color = 'grey',
            date_of_adoption = datetime.now())
        self.animal.save()
        self.animal.admin_data = self.admin
        self.animal.owner = self.owner
        self.animal.save()
        
    def test_get_animal_for_template(self):
        ''' tests if the function returns a list of animal objects '''
        list_animals = get_animals_for_template()
        self.assertEqual(list_animals[0], self.animal)

    def test_get_animal_from_given_id(self):
        ''' tests if the function returns a list of animal objects using a given id '''
        list_animals = get_animal_from_given_id(1)
        self.assertEqual(list_animals[0], self.animal)

class TestSheetForm(TestCase):  
    """ tests the methods from the class form SheetForm """
    def setUp(self):
        self.sf = SheetForm()
        self.sf.cleaned_data = {'caution': '0e', 'chip': '', 'date_of_adoption': datetime(2015, 6, 20).date(), \
        'date_of_birth': datetime(2015, 2, 15).date(), 'date_of_neuter': datetime(2015, 6, 22).date(), \
        'futur_date_of_neuter': None, 'file': 'g22h687', 'is_neutered': '1', \
        'mail': 'micro2@gmail.com', 'mail_reminder': 0, 'name': 'gims78', 'status': 'gims chante', \
        'owner_name': 'Miley', 'owner_surname': 'Krofon', 'owner_sex': 'H', 'observation': 'porte des lunettes', \
        'color': 'noir', 'race': 'gros batard', 'species': '1', 'tatoo': '777', 'phone': '0302010607', 'tel_reminder': 0}
        self.dict_values = self.sf.from_form()
    @skip
    def test_from_form(self):
        """ test if the function returns a dictionary of values to fill rows in tables,
        then test the key of each list_values"""
        dict_to_test = self.sf.from_form()
        list_keys = []
        for key in dict_to_test:
            list_keys.append(key)
        self.assertTrue(isinstance(dict_to_test, dict))
        self.assertEqual(['animal', 'admin', 'owner'], list_keys)
    @skip
    def test_save_data(self):
        """ tests if the function can save given classes in the db"""
        all_entries = Animal.objects.all()
        nb_entries = len(all_entries)
        output = self.sf.save_data(self.dict_values)
        all_entries2 = Animal.objects.all()
        nb_entries2 = len(all_entries2)
        self.assertTrue(nb_entries < nb_entries2)
    @skip
    def test_2nd_same_sheet_added(self): 
        """ test if the base will not be changed when 2nd same sheet tries to be add"""
        output = self.sf.save_data(self.dict_values)
        animal = Animal.objects.all()
        output2 = self.sf.save_data(self.dict_values)
        animal2 = Animal.objects.all()
        self.assertTrue('Erreur' in output2)
        self.assertTrue(len(animal) == len(animal2))

    def test_2nd_same_owner_added(self): 
        """ tests if 2nd sheet entries will be added if 2 diff animals have the same user """
        print("test_2nd_same_owner_added --")
        output = self.sf.save_data(self.dict_values)
        #2nd animal
        self.sf.cleaned_data['name'] = 'gims'
        self.sf.cleaned_data['file'] = 'gims123'
        self.dict_values = self.sf.from_form()
        output2 = self.sf.save_data(self.dict_values)
        print(output2)
        # all_entries = len(Animal.objects.all())
        # print(Animal.objects.all(), all_entries)
        # print("----")
        # self.assertTrue(all_entries == 2)


@skip
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

