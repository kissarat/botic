#!/usr/bin/env python3
import json
from telegram import config, call, send

if not call('getMe'):
    print('Unauthorized')
    exit(-1)

USERS_FILENAME = './users.json'

try:
    with open(USERS_FILENAME) as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

MODE_NOTHING = 0
MODE_READ_LAST_MESSAGE = 1


def get_user(username):
    return users[username] if username in users else {
        'mode': MODE_NOTHING,
        'last_message': None
    }


while True:
    for update in call('getUpdates', **config['updates']):
        config['updates']['offset'] = update['update_id'] + 1
        if 'message' in update:
            m = update['message']
            text = m['text']
            username = m['from']['username']
            chat_id = m['chat']['id']
            user = get_user(username)
            if MODE_READ_LAST_MESSAGE == user['mode']:
                user['mode'] = MODE_NOTHING
                found = get_user(text)
                if found['last_message'] is not None:
                    send(chat_id, 'User %s said "%s"' % (text, found['last_message']))
                else:
                    send(chat_id, 'User %s said nothing' % text)
                continue
            if text.startswith('/'):
                if '/read' == text:
                    user['mode'] = MODE_READ_LAST_MESSAGE
                    send(chat_id, 'Please, enter an username')
                elif '/start' == text:
                    send(chat_id, 'Hi, %s!' % username)
                else:
                    send(chat_id, 'Unknown command "%s"' % text)
            else:
                print('%s: %s' % (username, text))
                user['last_message'] = text
            users[username] = user
        else:
            print('Invalid update ' + json.dumps(update))
    with open(USERS_FILENAME, 'w') as f:
        json.dump(users, f, ensure_ascii=False, indent=2, sort_keys=True)
