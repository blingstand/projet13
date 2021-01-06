#this script regroup all url pages for seleniums


from selenium.webdriver.support.ui import WebDriverWait as wait
# from selenium.webdriver.common.keys import Keys


dict_btn = {
    "id_nav_sheet" : "/spa/sheet/index/", 
    "ajouter" : "/spa/sheet/index/add", 
}
dict_values = {
    "id_name" : "Sushi", 
    "id_color" : "blanc et noir", 
    "id_race" : "inconnue", 
    "id_date_of_birth": "01-01-2020", 
    "id_date_of_adoption": "01-02-2020", 
    "id_chip": "123123123456456456789",
    "id_is_neutered_1":0, 
    "id_species": "chatte",
    "id_status": "Sushi doit être stérilisée sous 15 jours.",
    "eye": 0, 
}
dict_values_owner = {
    'id_owner_name' : "Hadrien",
    'id_owner_surname' : "Clupot",
    'id_owner_sex' : "id_owner_sex_0",
    'id_phone' : "0646555999",
    'id_mail' : "adrien.clupot@mail.fr",
}
def click_on(self, target): 
    self.driver.find_element_by_id(target).click()

def navigate_when_click_on(name_button, previous_page, self):
    """click on a button and return the url of the page"""
    click_on(self, name_button)
    wait(self.driver, 3).until(lambda driver: 
        self.driver.current_url != previous_page)
    new_url = f"{self.live_server_url}{dict_btn[name_button]}"
    return new_url

def fill_add_owner_sheet_blank(self): 
    """ this function fills the owner blank"""  
    window_after = self.driver.window_handles[1]
    self.driver.switch_to_window(window_after)
    for id_input in dict_values_owner:
        print("\t--owner > ", id_input)
        if id_input == "id_owner_sex": 
            click_on(self, "id_owner_sex_0")
        else:
            self.driver.find_element_by_id(id_input).send_keys(dict_values_owner[id_input])
    click_on(self, "save")

def select_option(self, where, text):
    el = self.driver.find_element_by_id(where)
    for option in el.find_elements_by_tag_name('option'):
        
        if text in option.text.split(' '):
            option.click() # select() in earlier versions of webdriver
            break

def fill_add_sheet_blank(self):
    """ this function fills the blank"""
    for id_input in dict_values: 
        print("-- ", id_input)
        if id_input == "id_species": 
            select_option(self, 'id_species', dict_values['id_species'])
        elif id_input == "id_is_neutered_1":
            click_on(self, "id_is_neutered_1")
        elif id_input == "eye":
            #create a new owner
            window_before = self.driver.window_handles[0]
            click_on(self, "eye")
            fill_add_owner_sheet_blank(self)
            self.driver.switch_to_window(window_before)
            print("I refresh page ... ")
            self.driver.refresh()
            print("done !")
        else:
            selected_input = self.driver.find_element_by_id(id_input)
            selected_input.send_keys(dict_values[id_input])
    
   
    select_option(self, 'id_select_owner', "(id=1)")
    click_on(self, "save")
    

def fill_modify_sheet_blank(self):
    self.driver.find_element_by_id("id_caution").send_keys("100")
    click_on(self, "save")

def fill_modify_owner_sheet_blank(self):
    name_input = self.driver.find_element_by_id("id_owner_name")
    name_input.clear()
    name_input.send_keys("Adrien")
    click_on(self, "submit")

def add_new_contact(self):
    self.driver.find_element_by_id("id_date_2").send_keys("01-02-2020")
    select_option(self, "id_select_2", "propriétaire")
    self.driver.find_element_by_id("id_title_2").send_keys("date stérilisation")
    self.driver.find_element_by_id("id_area_2").send_keys(\
        "Sushi a une date de stérilisation pour fin février")
    click_on(self, "submit")

def modify_new_contact(self):
    input_date = self.driver.find_element_by_id("id_date_3")
    input_date.clear()
    input_date.send_keys("05-02-2020")
    click_on(self, "submit")