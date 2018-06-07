#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

'''
i = follow('trigger', 'key')
print(i.post())
'''

ENDPOINT = 'https://maker.ifttt.com/trigger/{0}/with/key/{1}'


class ifttt(object):
    def __init__(self, trigger, key):
        self.endpoint = ENDPOINT.format(trigger, key)

    def post(self, value1):
        post_params = {
            'value1': value1
        }
        r = requests.post(self.endpoint, params=post_params)
        return r.text
