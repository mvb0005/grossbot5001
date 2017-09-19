import os
import json
import psycopg2
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

con = psycopg2.connect(os.environ["DATABASE_URL"])

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
                            i = ""
                            cur = con.cursor()
                            cur.execute("""SELECT * FROM BREATHE""")
                            rows = cur.fetchall()
                            b_in = int([y for x,y in rows if x == "Breath_In"][0])
                            b_out = int([y for x,y in rows if x == "Breath_Out"][0])
                            b_in += int(text.split()[3])
                            b_out += int(text.split()[5])
                            cur.execute("""
                                UPDATE Breathe
                                SET value=%s
                                WHERE id=%s
                            """, (str(b_in),"Breath_In"))
                            cur.execute("""
                                UPDATE Breathe
                                SET value=%s
                                where id=%s
                            """, (str(b_out),"Breath_Out"))
                            con.commit()
                            con.close()
                            msg = ("Don't Forget To BREATHE!" +
                                   " We have breathed in for {} and out" +
                                   " for {}, enough to play the fight song" +
                                   " {} times.").format(b_in, b_out, float(b_out)/64.0)
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
