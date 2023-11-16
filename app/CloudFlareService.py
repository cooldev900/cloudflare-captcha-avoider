from app.setting import API_KEY
# from smsactivate.api import SMSActivateAPI
import requests
# import re
import json


class CloudFlareService:
    def __init__(self):
        self.url = "https://2captcha.com/in.php"
        

    def get_captcha_id(self, sitekey):
        param = {
            "key": API_KEY,
            "method": "turnstile",
            "sitekey": sitekey,
            "pageurl": "https://2captcha.com/demo/cloudflare-turnstile",
            "json": 1
        }

        r = requests.post(self.url, params=param)
        result = json.loads(r.text)
        print(result)
        if result.get('status') == 1:
            return result.get('request')
        else:
            return ""

    def get_cloud_token(self, id):
        r = requests.get(f'https://2captcha.com/in.php?key={API_KEY}&action=get&id={id}&json=1')
        result = json.loads(r.text)
        print(result)
        if result.get('status') == 1:
            return result.get('request')
        else:
            return ""

        

