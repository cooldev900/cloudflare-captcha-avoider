from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from app.setting import HAPPN_URL, COUNTRIES, CODES
from app.SMSService import SMSService
import os


class AccountCreator:
    def __init__(self):
        self.name = "AccountCreator"
        self.sms_service = SMSService("SMS Activator")
        self.browser = webdriver.Chrome()
        self.browser.get(HAPPN_URL)
        self.wait = WebDriverWait(self.browser, 30)
        self.personal_info = {
            'day': '11',
            'month': '3',
            'year': '2021',
            'first_name': 'Lousia',
            'gender': 'male',
        }

    def __del__(self):
        time.sleep(10)
        self.browser.close()

    def get_sms_code(self, activation_id):
        retry_count = 0
        while True:
            activation_status = self.sms_service.sms_activate_service.getStatus(
                id=activation_id)
            print(
                f'activationId: {activation_id}, status: {activation_status}')
            if activation_status.startswith('STATUS_OK'):
                return activation_status.replace('STATUS_OK:', '')
            if activation_status == 'STATUS_WAIT_CODE':
                time.sleep(5)
                retry_count += 1
            if retry_count == 6:
                return ""

    def create_happn_account(self):
        if self.sms_service.balance == 0:
            print("You don't have enough balance.")

        # click accept button
        accept_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="button"]')))
        accept_button.click()
        time.sleep(1)

        # click Sign in button
        sign_in_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="btn-sign-in"]')))
        sign_in_button.click()
        time.sleep(5)

        # click Use my phone number
        use_phone_number_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="btn-login-sms"]')))
        use_phone_number_button.click()
        time.sleep(1)

        # click I agree to these terms
        agree_terms_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="btn-accept-tos"]')))
        agree_terms_button.click()
        time.sleep(1)

        # click Continue
        continue_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="btn-accept-cookies"]')))
        continue_button.click()
        time.sleep(5)

        # get top countries for happn service
        # for service_data in self.sms_service.top_countries_for_service.values():
            # enter phone number and get activation code
            # {'country': 78, 'count': 6406, 'price': 5, 'retail_price': 10}
            # if service_data.get('country') == 78:
            #     continue
            # count = service_data.get('count')
            # code = ''
            # while count > 0:
                # phone_number = self.sms_service.get_virtual_number(service_data.get('country'))
        phone_number = {'activationId': '1878578568', 'phoneNumber': '12056269972', 'activationCost': '10.00', 'countryCode': '12', 'canGetAnotherSms': True, 'activationTime': '2023-11-08 05:06:12', 'activationOperator': 'tim'}
                # activation_id = phone_number.get('activationId')
                # print(f'activationID {activation_id}')
        self.enter_phone_number(phone_number)
        time.sleep(60)
                # time.sleep(30)
                # code = self.get_sms_code(activation_id)
                # print(f'code: {code}')
                # if not code:
                #     count -= 1
                #     self.browser.back()
                #     time.sleep(1)
                # else:
        self.continue_registration_with_sms_code(self.personal_info)
                    # return

        # print(f'code: {code}')

    def enter_phone_number(self, phone_number):
        country_name = COUNTRIES.get(phone_number.get('countryCode'))
        country_code = CODES.get(phone_number.get('countryCode'))
        print(phone_number)
        print(country_name)
        print(country_code)
        if "USA" in country_name:
            country_name = "United States"

        self.wait.until(EC.url_to_be("https://happn.app/registration/phone"))
        # set country code
        country_select_picker = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@data-testid="country-select-picker-opener"]')))
        country_select_picker.click()
        time.sleep(1)

        # Find a country
        country_search_input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@data-testid="country-picker-search-input"]')))
        time.sleep(1)
        country_search_input.send_keys(country_name)
        time.sleep(1)
        print(f'//div[@data-testid="{country_code}"]')
        country_code_selector = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//div[@data-testid="{country_code}"]')))
        print(
            f'country selector html {country_code_selector.get_attribute("outerHTML")}')

        country_number_div = country_code_selector.find_element(
            By.XPATH, f'//div[@data-testid="{country_code}"]/div[1]')
        country_number = country_number_div.get_attribute("innerHTML")
        print(f'country selector html {country_number}')

        phone_number_without_country_number = phone_number.get('phoneNumber')[
            len(country_number) - 1:]
        print(f'country selector html {phone_number_without_country_number}')
        country_code_selector.click()
        time.sleep(1)

        phone_number_input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@data-testid="phone-number-input"]')))
        phone_number_input.send_keys(phone_number_without_country_number)
        time.sleep(1)

        continue_button_in_phone_number = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="btn-submit-registration-phone"]')))
        print(f'{continue_button_in_phone_number.get_attribute("outerHTML")}')
        if continue_button_in_phone_number.is_enabled() == False:
            print("false")
            time.sleep(2)
        continue_button_in_phone_number.click()
        self.sms_service.sms_activate_service.setStatus(id=phone_number.get('activationID'),status=1)
        time.sleep(1)

    def continue_registration_with_sms_code(self, personal_info):
        # self.wait.until(EC.url_to_be(
        #     "https://happn.app/registration/phone/verify"))
        # code_divs = self.wait.until(EC.visibility_of_element_located(
        #     (By.XPATH, '//div[@data-testid="code-input"]')))
        # input1 = code_divs.find_element(By.XPATH, '//div/input[1]')
        # input1.send_keys(sms_code[0])
        # input2 = code_divs.find_element(By.XPATH, '//div/input[2]')
        # input2.send_keys(sms_code[1])
        # input3 = code_divs.find_element(By.XPATH, '//div/input[3]')
        # input3.send_keys(sms_code[2])
        # input4 = code_divs.find_element(By.XPATH, '//div/input[4]')
        # input4.send_keys(sms_code[3])
        # time.sleep(1)

        # continue_button_in_phone_number = self.wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, '//button[@data-testid="btn-submit-registration-phone"]')))
        # print(f'{continue_button_in_phone_number.get_attribute("outerHTML")}')
        # if continue_button_in_phone_number.is_enabled() == False:
        #     print("false")
        #     time.sleep(2)
        # continue_button_in_phone_number.click()
        # time.sleep(1)

        self.wait.until(EC.url_to_be(
            "https://happn.app/registration/birth-date"))
        day_input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@data-testid="dateInput-day"]')))
        day_input.send_keys(personal_info.get('day'))
        month_input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@data-testid="dateInput-month"]')))
        month_input.send_keys(personal_info.get('month'))
        year_input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@data-testid="dateInput-year"]')))
        year_input.send_keys(personal_info.get('year'))
        time.sleep(1)

        continue_birth_registration_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="btn-submit-registration-birthDate"]')))
        print(f'{continue_birth_registration_button.get_attribute("outerHTML")}')
        if continue_birth_registration_button.is_enabled() == False:
            print("false")
            time.sleep(2)
        continue_birth_registration_button.click()
        time.sleep(1)

        first_name_input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@data-testid="input-registration-firstname"]')))
        first_name_input.send_keys(personal_info.get('first_name'))
        time.sleep(1)

        self.wait.until(EC.url_to_be(
            "https://happn.app/registration/first-name"))
        continue_first_registration_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="btn-submit-registration-birthDate"]')))
        print(f'{continue_first_registration_button.get_attribute("outerHTML")}')
        if continue_first_registration_button.is_enabled() == False:
            print("false")
            time.sleep(2)
        continue_first_registration_button.click()
        time.sleep(1)
        # should be male or femail
        gender_select_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//button[@data-testid="btn-{personal_info.get("gender")}"]')))
        gender_select_button.click()
        time.sleep(1)

        self.wait.until(EC.url_to_be("https://happn.app/registration/gender"))
        continue_gender_registration_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="button"]')))
        print(f'{continue_gender_registration_button.get_attribute("outerHTML")}')
        if continue_gender_registration_button.is_enabled() == False:
            print("false")
            time.sleep(2)
        continue_gender_registration_button.click()
        time.sleep(1)

        # matching-preferences
        self.wait.until(EC.url_to_be(
            "https://happn.app/registration/pictures"))
        man_preferce_selector = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//button[@data-testid="switch-male"]')))
        man_preferce_selector.click()
        female_preferce_selector = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//button[@data-testid="switch-female"]')))
        female_preferce_selector.click()
        time.sleep(1)

        continue_matching_preferences_registration_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="button"]')))
        print(
            f'{continue_matching_preferences_registration_button.get_attribute("outerHTML")}')
        if continue_matching_preferences_registration_button.is_enabled() == False:
            print("false")
            time.sleep(2)
        continue_matching_preferences_registration_button.click()
        time.sleep(1)

        # registration/pictures
        self.wait.until(EC.url_to_be(
            "https://happn.app/registration/pictures"))
        for value in [1, 2]:
            upload_file = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", f"photo/{value}.jpeg"))
            print(f'file path: {upload_file}')
            image_input = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//input[@type="file"]')))
            image_input.send_keys(upload_file)
            time.sleep(1)

            add_to_profile_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="btn-modal-confirm-crop"]')))
            add_to_profile_button.click()
            time.sleep(2)

        continue_picture_registration_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="btn-submit-pictures"]')))
        print(f'{continue_picture_registration_button.get_attribute("outerHTML")}')
        if continue_picture_registration_button.is_enabled() == False:
            print("false")
            time.sleep(2)
        continue_picture_registration_button.click()
        time.sleep(1)