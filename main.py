#!/usr/bin/env python3
import json
from telegram import config, call, send

if not call('getMe'):
    print('Unauthorized')
    exit(-1)

messages = {}

usernameReader = 0

while True:
    for update in call('getUpdates', **config['updates']):
        config['updates']['offset'] = update['update_id'] + 1
        if 'message' in update:
            m = update['message']
            text = m['text']
            username = m['from']['username']
            chat_id = m['chat']['id']
            if chat_id == usernameReader:
                usernameReader = 0
                if text in messages:
                    send(chat_id, 'User %s said "%s"' % (text, messages[text]))
                else:
                    send(chat_id, 'User %s said nothing' % text)
                continue
            if text.startswith('/'):
                if '/read' == text:
                    usernameReader = chat_id
                    send(chat_id, 'Please, enter an username')
                elif '/start' == text:
                    send(chat_id, 'Hi, %s!' % username)
                else:
                    send(chat_id, 'Unknown command "%s"' % text)
            else:
                print('%s: %s' % (username, text))
                messages[username] = text
        else:
            print('Invalid update ' + json.dumps(update))
