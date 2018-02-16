#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import nfc
import nfc.ndef
import os
import time
import urllib
import urllib2
import yaml
import follow
from datetime import datetime

log_format = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='shussha_follow.log', level=logging.DEBUG, format=log_format)
dirpath = os.path.abspath(os.path.dirname(__file__))
conf = yaml.load(open(dirpath + '/conf.yml').read())
d_conf = yaml.load(open(dirpath + '/debug.yml').read())


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
            return
        logging.info('NFC ID: %s' % ic_id)
    except:
        logging.warn('Exception: While parsing ID.')
        time.sleep(5)
        return

    if ic_id not in conf:
        text = 'Not registerd NFC ID: %s' % ic_id
        logging.info(text)

        params = urllib.urlencode({
            'token': d_conf['debug']['token'],
            'channel': d_conf['debug']['channel'].encode('utf-8'),
            'icon_url': d_conf['debug']['icon_url'],
            'username': d_conf['debug']['username'],
            'text': text,
        })
        post_slack(params)
        time.sleep(5)
        return

    current_hour = int(datetime.now().strftime("%H"))
    if current_hour < conf[ic_id]['time_period']:
        channel = '#出勤連絡'
        dakoku_type = 0
    else:
        channel = '#退勤連絡'
        dakoku_type = 1

    f = follow(conf[ic_id]['company_id'], conf[ic_id]['login_id'], conf[ic_id]['password'])
    f.login()
    res = f.dakoku(dakoku_type)
    logging.info('%r' % res)

    params = urllib.urlencode({
        'token': conf[ic_id]['token'],
        'channel': channel,
        'text': conf[ic_id]['text'],
        'as_user': 'true',
    })
    post_slack(params)
    time.sleep(5)


def released(tag):
    print("released:")


def post_slack(params):
    url = 'https://slack.com/api/chat.postMessage'
    req = urllib2.Request(url, params, {'Content-type': 'application/x-www-form-urlencoded'})
    res = urllib2.urlopen(req)
    logging.info('%r' % res.read())
    logging.info('posted.')


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
