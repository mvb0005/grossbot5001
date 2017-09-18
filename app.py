import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    text = str(data['text'])

    if data['name'] != "Test":
        if text[:3].lower() == '@tn':
            if len(text.split()) >= 6 and text.split()[1].lower() == "breathe":
                if text.split()[2].lower() == "in":
                    if text.split()[4].lower() == "out":
                        if text.split()[3].isdigit() and text.split()[5].isdigit():
                            f = open('breathe.txt' , 'r')
                            i = f.read()
                            b_in = 0
                            b_out = 0
                            if len(i.split()) == 2:
                                if i.split()[0].isdigit() and i.split()[1].isdigit():
                                    b_in = int(i.split()[0])
                                    b_out = int(i.split()[1])
                            b_in += int(text.split()[3])
                            b_out += int(text.split()[5])
                            f.close()
                            f = open('breathe.txt' , 'w')
                            f.write(str(b_in) + " " + str(b_out))
                            msg = ("Don't Forget To BREATHE!" +
                                   " We have breathed in for {} and out" +
                                   " for {}, enough to play the fight song" +
                                   " {} times.").format(b_in, b_out, float(b_out)/64.0)
                            send_message(msg)
                            return

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
