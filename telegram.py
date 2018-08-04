import requests
import json

with open('./config.json') as f:
    config = json.load(f)


def call(method, **params):
    r = requests.get('https://api.telegram.org/bot%s/%s' % (config['token'], method), params=params)
    data = r.json()
    return data['result'] if data['ok'] else None


def send(chat_id, text):
    call('sendMessage', chat_id=chat_id, text=text)
