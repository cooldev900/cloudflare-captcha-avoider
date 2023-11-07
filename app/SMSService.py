from app.setting import SMS_ACTIVATE_API_KEY
from smsactivate.api import SMSActivateAPI
import requests
import re
import json


class SMSService:
    def __init__(self, name):
        self.name = name
        self.happn_service_code = "df"
        self.sms_activate_service = SMSActivateAPI(
            SMS_ACTIVATE_API_KEY)
        try:
            self.top_countries_for_service = self.sms_activate_service.getTopCountriesByService(
                service=self.happn_service_code, freePrice=True)
        except:
            self.top_countries_for_service = {}

        try:
            balance = self.sms_activate_service.getBalanceAndCashBack()
            print(balance)
            self.balance = float(balance.get('balance'))
        except:
            self.balance = 0

    def get_virtual_number(self, country):
        number = {'activationId': '', 'phoneNumber': ''}
        
        while not number.get('activationId') and not number.get('phoneNumber'):
            try:
                number = self.sms_activate_service.getNumberV2(service=self.happn_service_code, country=country)
            except:
                number = {'activationId': '', 'phoneNumber': ''}
        
        return number

    def get_code_from_message(self, message):
        match = re.search(r'\d+', message)
        code = ''
        if match:
            code = match.group()
        return code


    def get_sms_code_from_history(self, activation_id):
        print(f'activationId: {activation_id}')
        payload = {'api_key': SMS_ACTIVATE_API_KEY, 'action': 'getHistory'}
        r = requests.get("https://api.sms-activate.org/stubs/handler_api.php", params=payload)
        result = json.loads(r.text) 
        filtered = [row for row in result if row.get('id') == int(activation_id)]
        last_row = filtered[-1]
        print(last_row)
        return self.get_code_from_message(last_row.get('sms'))

