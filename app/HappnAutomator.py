import setting
from smsactivate.api import SMSActivateAPI


class HappnAutomator:
    def __init__(self, name):
        self.name = name
        self.happn_service_code = "df"
        self.sms_activate_service = SMSActivateAPI(
            setting.SMS_ACTIVATE_API_KEY)
        try:
            self.top_countries_for_service = self.sms_activate_service.getTopCountriesByService(
                service=self.happn_service_code, freePrice=True)
        except:
            self.top_countries_for_service = {
                0: {'country': 78, 'count': 6406, 'price': 5, 'retail_price': 10}
            }

        try:
            balance = self.sms_activate_service.getBalanceAndCashBack()
            self.balance = float(balance.balance)
        except:
            balance = 0

    def get_virtual_number(self):
        number = {'activationId': '', 'phoneNumber': ''}
        while number['activationId'] == '' and number['phoneNumber'] == '':
            try:
                number = self.sms_activate_service.getNumberV2(
                    service=self.happn_service_code, phoneException=0)
            except:
                number = {'activationId': '', 'phoneNumber': ''}
        return number
