#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import nfc
import os
import time
import yaml
from ifttt import ifttt
from follow import follow
from datetime import datetime

log_format = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='shussha.log', level=logging.DEBUG, format=log_format)
dirpath = os.path.abspath(os.path.dirname(__file__))
conf = yaml.load(open(dirpath + '/conf.yml').read())


def startup(targets):
    print('Waiting for new NFC tags...')
    return targets


def connected(tag):
    try:
        # ICカードのIDとしてsensf_res, またはsdd_resの取得を試みる
        ic_id = None
        for i in str(tag.target).split():
            if len(i.split('sensf_res=')) == 2:
                ic_id = i.split('sensf_res=')[1]
                break
            if len(i.split('sdd_res=')) == 2:
                ic_id = i.split('sdd_res=')[1]
                break

        if ic_id is None:
            logging.warn('Couldn\'t get sensf_res or sdd_res id.')
            time.sleep(5)
            return True
        logging.info('NFC ID: %s' % ic_id)
    except:
        logging.warn('Exception: While parsing ID.')
        time.sleep(5)
        return False

    if ic_id not in conf:
        text = 'Not registerd NFC ID: %s' % ic_id
        logging.info(text)
        time.sleep(5)
        return True

    current_hour = int(datetime.now().strftime("%H"))
    if current_hour < conf[ic_id]['time_period']:
        dakoku_type = 0
        value1 = '出勤'
    else:
        dakoku_type = 1
        value1 = '退勤'

    # POST follow
    f = follow(conf[ic_id]['follow']['company_id'], conf[ic_id]['follow']['login_id'], conf[ic_id]['follow']['password'])
    f.login()
    res = f.dakoku(dakoku_type)
    logging.info('%r' % res)

    # POST IFTTT
    if res.status_code == '200' and 'ifttt' in conf[ic_id]:
        i = ifttt(conf[ic_id]['ifttt']['trigger'], conf[ic_id]['ifttt']['key'])
        res = i.post(value1)
        logging.info('%r' % res)

    time.sleep(5)
    return True


def released(tag):
    print("released:")


if __name__ == '__main__':
    clf = nfc.ContactlessFrontend('usb')
    print(clf)

    if clf:
        while clf.connect(rdwr={
            'on-startup': startup,
            'on-connect': connected,
            'on-release': released,
        }):
            pass
