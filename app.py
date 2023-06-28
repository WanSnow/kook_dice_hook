import random
import re
import requests

from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello, World"


@app.route("/dice_hook", methods=['POST'])
def dice_hook():
    data = request.get_data()
    print(data)
    json_re = json.loads(data)

    print(json_re)

    d_channel_type = json_re['d']['channel_type']

    if d_channel_type == "GROUP":
        d_type = json_re['d']['type']
        content = json_re['d']['content']
        target_id = json_re['d']['target_id']
        msg_id = json_re['d']['msg_id']
        nonce = json_re['d']['nonce']

        if d_type == 1:
            g = re.match(r'\.r(\d*)d(\d*)', content, re.I)
            count = g.group(1)
            surface = g.group(2)
            if count == '':
                count = 1
            else:
                count = int(count)

            if surface == '':
                surface = 100
            else:
                surface = int(surface)

            msg = "["
            result = 0
            for num in range(1, count):
                dice = random.randint(1, surface)
                result += dice
                if num == 1:
                    msg += dice
                else:
                    msg += '+' + str(dice)

            msg += ']=' + str(result)

            headers = {'Content-Type': 'application/json', 'Authorization': 'Bot 1/MTg3MTY=/PzC/dTlYQxdFzSfQwYXUTQ=='}
            data = {'type': 1, 'target_id': target_id, 'content': msg, 'quote': msg_id, 'nonce': nonce}

            requests.post("https://www.kookapp.cn/api/v3/message/create", headers=headers, data=data)

    return {
        "challenge": json_re['d']['challenge']
    }
