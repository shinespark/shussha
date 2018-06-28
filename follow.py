#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

'''
f = follow('company_id', 'login_id', 'password')
f.login()
print(f.dakoku(1))
'''

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
LOGIN_URL = 'https://follow.jp/cw/login'
SERVLET_URL = 'https://follow.jp/cw/servlet'


class follow(object):
    def __init__(self, company_id, login_id, password):
        self.company_id = company_id
        self.login_id = login_id
        self.password = password
        self.headers = {'User-Agent': USER_AGENT}
        self.cookies = None

    def login(self):
        login_data = {
            'companyID': self.company_id,
            'loginID': self.login_id,
            'passwdID': self.password,
            'service_key_event': 'passok',
            'browserType': '',
            'companyChkId': 1,
            'loginChkID': 1
        }
        r = requests.post(LOGIN_URL, params=login_data, headers=self.headers)
        self.cookies = r.cookies

    def dakoku(self, dakoku_type):
        dakoku_data = {
            'clockOnTarget': dakoku_type,
            'syainCode': self.login_id,
            'SCID': 'STC_M'
        }
        res = requests.post(SERVLET_URL, params=dakoku_data, headers=self.headers, cookies=self.cookies)

        if res.status_code == '200':
            return res.text
        else:
            return False
