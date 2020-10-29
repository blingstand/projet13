import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

path_to_chrome = '/home/blingstand/Bureau/projets/oc/projet13/tests/chromedriver'
print(os.environ["PATH"])
class AccountTestCase(StaticLiveServerTestCase):
    def setUp(self):
        NEW_USER = User(username="test")
        NEW_USER.set_password("test")
        NEW_USER.save()
        self.driver = webdriver.Chrome(path_to_chrome)
    def test_login(self):
        print(self.live_server_url)
        connection = f"{self.live_server_url}/spa/user/connection"
        self.driver.get(connection)

        username = self.driver.find_element_by_id('id_username')
        password = self.driver.find_element_by_id('id_password')
        submit = self.driver.find_element_by_id('id_submit')

        username.send_keys('test')
        password.send_keys('test')
        submit.send_keys(Keys.RETURN)
        wait(self.driver, 2).until(lambda driver: self.driver.current_url != connection)
        
        if self.driver.current_url == connection:
            self.driver.quit()