from selenium import webdriver
import setting

class AccountCreator:
    def __init__(self):
        self.name = "AccountCreator"
        driver = webdriver.Chrome()

        driver.get("http://selenium.dev")

        driver.quit()