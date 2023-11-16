from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from app.CloudFlareService import CloudFlareService


class CloudFlareAvoider:
    def __init__(self):
        self.name = "VSF"
        self.browser = webdriver.Chrome()
        self.browser.get("https://visa.vfsglobal.com/gbr/en/ita/login")
        self.wait = WebDriverWait(self.browser, 30)
        self.cloudFlareService = CloudFlareService()

    def __del__(self):
        time.sleep(10)
        self.browser.close()


    def workflow(self):
        # click accept button
        accept_cookie_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')))
        accept_cookie_button.click()
        time.sleep(1)
        
        name_input = self.wait.until((EC.visibility_of_element_located((By.XPATH, '//input[@formcontrolname="username"]'))))
        time.sleep(1)
        name_input.send_keys("tavomiv149@jucatyo.com")

        password = self.wait.until((EC.visibility_of_element_located((By.XPATH, '//input[@formcontrolname="password"]'))))
        time.sleep(1)
        password.send_keys("homvzSt!Joj3Nm")      


        iframe = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe[src*="https://challenges.cloudflare.com/cdn-cgi/challenge-platform"]')))
        
        print(iframe.get_attribute('outerHTML'))

        src = iframe.get_attribute('src')
        print(src)

        sitekey = src.split("/")[-3]

        print(sitekey)

        captcha_id = self.cloudFlareService.get_captcha_id(sitekey=sitekey)
        if not captcha_id:
            print("Fetching sitekey id failed")
            return ""
        
        token = self.cloudFlareService.get_cloud_token(id=captcha_id)

        # if not token:
        #     print("Fetch Token failed")
        #     # return ""
        
        # script = f'document.getElementsByName("cf-turnstile-response")[0].value="something"'

        # self.browser.execute_script(script)

        signin_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@mat-stroked-button]")))
        signin_button.click()
        time.sleep(10)


    