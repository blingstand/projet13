import os
import time
from datetime import datetime
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .utils_for_selenium import *

path_to_chrome = '/home/blingstand/Bureau/projets/oc/projet13/tests/chromedriver'

class AccountTestCase(StaticLiveServerTestCase):
    def setUp(self):
        NEW_USER = User(username="test")
        NEW_USER.set_password("test")
        NEW_USER.save()
        self.driver = webdriver.Chrome(path_to_chrome)
    @skip
    def test_rapid_test(self):
        self.driver.get(f"{self.live_server_url}/spa/sheet/index/add")
        fill_add_sheet_blank(self)


    # @skip
    def test_user_stories(self):
        start = datetime.now()
        """all test using seleniums"""
        #****************************
        #       TEST LOGIN 
        #****************************
        connection_url = f"{self.live_server_url}/spa/user/connection"
        self.driver.get(connection_url)

        username = self.driver.find_element_by_id('id_username')
        password = self.driver.find_element_by_id('id_password')
        submit = self.driver.find_element_by_id('id_submit')

        username.send_keys('test')
        password.send_keys('test')
        submit.send_keys(Keys.RETURN)
        wait(self.driver, 20).until(lambda driver: self.driver.current_url != connection_url)
        dashboard_url = f"{self.live_server_url}/spa/mydashboard/"
        self.assertEqual(
            self.driver.current_url,dashboard_url)
        print("test login ok")

        #****************************
        #       TEST SHEET APP 
        #****************************
        
        #click nav sheet btn
        # > navigate_when_click_on_(button_clicked, previous_page, tester)
        sheet_index_url = navigate_when_click_on(
            'id_nav_sheet', dashboard_url, self)
        self.assertEqual(self.driver.current_url, sheet_index_url)
        print("test > bouton sheet nav ok")
        
        #click add sheet btn
        add_sheet_url = navigate_when_click_on(
            'ajouter', sheet_index_url, self)
        self.assertEqual(self.driver.current_url, add_sheet_url)
        print("test > bouton add sheet ok")

        fill_add_sheet_blank(self)
        print("test > add sheet ok ")

        #click on modify button
        click_on(self, "1")
        click_on(self, "modifier")
        fill_modify_sheet_blank(self)
        print("test > modify sheet ok")
        
        #click on display button
        click_on(self, "display")
        print("test > display btn ok")

        #click on modify button (for owner)
        click_on(self, "ow1")
        click_on(self, "modifier")
        fill_modify_owner_sheet_blank(self)
        print("test > modify sheet ok")

        click_on(self, "id_contact_1")
        click_on(self, "ajouter")
        add_new_contact(self)
        wait(self.driver, 3).until(lambda driver: 
        self.driver.find_element_by_id("id_contact_2") != None)
        print("test > add contact ok")

        click_on(self, "id_contact_2")
        click_on(self, "modifier")
        modify_new_contact(self)
        print("test > modify contact ok")

        click_on(self, "supprimer")
        alert_obj = self.driver.switch_to.alert
        alert_obj.accept()
        print("test > alert msg click delete ok")

        wait(self.driver, 3).until(lambda driver: 
        self.driver.find_element_by_id("id_contact_2") != None)
        click_on(self, "id_contact_2")
        click_on(self, "supprimer")
        print("test > confirmation msg click delete ok")
        alert_obj = self.driver.switch_to.alert
        alert_obj.accept()

        click_on(self, "id_nav_mail")
        input("bon ?")

        #****************************
        #       TEST MAIL APP 
        #****************************
        
        end = datetime.now()
        input(f"temps d'exécution : {(end-start)}")
        return None
        

        click_on(self, "display2")
        time.sleep(2)

        #click on delete button
        click_on(self, "1")
        click_on(self, "supprimer")
        alert_obj = self.driver.switch_to.alert
        alert_obj.accept()
        input("test delete sheet ok")
        







         


