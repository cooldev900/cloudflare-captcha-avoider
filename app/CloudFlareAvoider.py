from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from app.CloudFlareService import CloudFlareService
from twocaptcha import TwoCaptcha
from app.setting import API_KEY
from undetected_chromedriver import Chrome, ChromeOptions


class CloudFlareAvoider:
    def __init__(self):
        self.name = "VSF"
        self.url = "https://visa.vfsglobal.com/gbr/en/ita/login"
        self.site_key = "0x4AAAAAAACYaM3U_Dz-4DN1"
        # self.cloudFlareService = CloudFlareService()
        self.solver = TwoCaptcha(API_KEY)
        self.setup()

    def __del__(self):
        time.sleep(10)
        self.browser.close()

    def setup(self):    
        # Initialize the WebDriver
        chrome_options = ChromeOptions()
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
        chrome_options.headless = False
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--lang=en-US,en;q=0.9")
        chrome_options.add_argument("--window-size=1024,768")
        self.browser = Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 200)
    
        try:
            self.inject_turnstile_script()
            captcha_id, token = self.solve_turnstile()
            if captcha_id:
                self.browser.get(self.url)
                time.sleep(5)
                self.handle_turnstile_callback(token)
        finally:
            self.login()


    def login(self):
        self.wait.until(EC.url_to_be(self.url))
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

        signin_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@mat-stroked-button]")))
        signin_button.click()
        time.sleep(200)

    def solve_turnstile(self):
        try:
            result = self.solver.turnstile(
                sitekey=self.site_key,
                url=self.url
            )
    
            if "captchaId" in result and "code" in result:
                captcha_id = result["captchaId"]
                code = result["code"]
                print(f"Solved FunCaptcha. Captcha ID: {captcha_id}, Code: {code}")
                return captcha_id, code
            else:
                print(f"Unexpected response format: {result}")
                return None
        except Exception as e:
            print(f"Error solving turnstile: {e}")
            return None

    def handle_turnstile_callback(self, token):
        callback_script = f"window.tsCallback('{token}')"
        self.browser.execute_script(callback_script)
 
    def inject_turnstile_script(self):
        # Inject the provided JavaScript code into the page
        script = """
        const i = setInterval(()=>{
            if (window.turnstile) {
                clearInterval(i)
                window.turnstile.render = (a, b) => {
                    let p = {
                        type: "TurnstileTaskProxyless",
                        websiteKey: b.sitekey,
                        websiteURL: window.location.href,
                        data: b.cData,
                        pagedata: b.chlPageData,
                        action: b.action,
                        userAgent: navigator.userAgent
                    }
                    console.log(JSON.stringify(p))
                    window.tsCallback = b.callback
                    return 'foo'
                }
            }
        }, 10)
        """
        self.browser.execute_script(script)


    