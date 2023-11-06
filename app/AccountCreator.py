from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from app.setting import HAPPN_URL, COUNTRIES, CODES
from app.SMSService import SMSService

class AccountCreator:
    def __init__(self):
        self.name = "AccountCreator"
        self.sms_service = SMSService("SMS Activator")
        self.browser = webdriver.Chrome()
        self.browser.get(HAPPN_URL)
        self.wait = WebDriverWait(self.browser, 30)

    def __del__(self):
        time.sleep(10)
        self.browser.close()        

    def create_happn_account(self):
        if self.sms_service.balance == 0:
            print("You don't have enough balance.")
        
        #click accept button
        accept_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="button"]')))
        accept_button.click()
        time.sleep(1)

        #click Sign in button
        sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="btn-sign-in"]')))
        sign_in_button.click()
        time.sleep(5)

        #click Use my phone number
        use_phone_number_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="btn-login-sms"]')))
        use_phone_number_button.click()
        time.sleep(1)

        #click I agree to these terms
        agree_terms_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="btn-accept-tos"]')))
        agree_terms_button.click()
        time.sleep(1)

        #click Continue
        continue_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="btn-accept-cookies"]')))
        continue_button.click()
        time.sleep(5)

        self.enter_phone_number()

    def enter_phone_number(self):

        phone_number = self.sms_service.get_virtual_number()
        country_name = COUNTRIES.get(phone_number.get('countryCode'))
        country_code = CODES.get(phone_number.get('countryCode'))
        print(phone_number)
        print(country_name)
        print(country_code)
        if "USA" in country_name:
            country_name = "United States"

        #set country code
        country_select_picker = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="country-select-picker-opener"]')))
        country_select_picker.click()
        time.sleep(1)

        #Find a country
        country_search_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@data-testid="country-picker-search-input"]')))
        time.sleep(1)
        country_search_input.send_keys(country_name)
        time.sleep(1)
        print(f'//div[@data-testid="{country_code}"]')
        country_code_selector = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[@data-testid="{country_code}"]')))
        print(f'country selector html {country_code_selector.get_attribute("outerHTML")}')

        country_number_div = country_code_selector.find_element(By.XPATH, f'//div[@data-testid="{country_code}"]/div[1]')
        country_number = country_number_div.get_attribute("innerHTML")
        print(f'country selector html {country_number}')

        phone_number_without_country_number = phone_number.get('phoneNumber')[len(country_number):]
        print(f'country selector html {phone_number_without_country_number}')
        country_code_selector.click()
        time.sleep(1)

        phone_number_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@data-testid="phone-number-input"]')))
        phone_number_input.send_keys(phone_number_without_country_number)
        time.sleep(1)

        continue_button_in_phone_number = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="btn-submit-registration-phone"]')))
        print(f'{continue_button_in_phone_number.get_attribute('outerHTML')}')
        if continue_button_in_phone_number.is_enabled() == False:
            print("false")
            time.sleep(2)
        continue_button_in_phone_number.click()



        









        
