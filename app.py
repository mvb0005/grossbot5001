import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    text = data['text']

    if data['name'] != "Test":
        if text[:3].lower() == '@tn':
            msg = '{}, ECHO: {}'.format(data['name'], data['text'])
            send_message(msg)

    return "ok", 200

def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
            'bot_id' : os.getenv('BOT_ID'),
            'text'   : msg,
           }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()
