#!/usr/bin/env python3
import requests
import json

with open('./config.json') as f:
    config = json.load(f)


def telegram(method, **params):
    r = requests.get('https://api.telegram.org/bot%s/%s' % (config['token'], method), params=params)
    data = r.json()
    return data['result'] if data['ok'] else None


if not telegram('getMe'):
    print('Unauthorized')
    exit(-1)

while True:
    for update in telegram('getUpdates', **config['updates']):
        config['updates']['offset'] = update['update_id'] + 1
        if 'message' in update:
            m = update['message']
            print('%s: %s' % (m['from']['username'], m['text']))
        else:
            print('Invalid update ' + json.dumps(update))
