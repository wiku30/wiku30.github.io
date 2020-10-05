#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import hashlib
import os.path
import random
import string
import requests

from flask import Flask, abort, request

FLAG = SECRET1
THE_ID = SECRET2

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 512

def proxy(url, request):
    params = dict(request.args)
    params.pop("url", None)
    headers = dict(request.headers)
    headers.pop("Host", None)
    try:
        if request.method == "GET":
            res = requests.get(url, params=params, headers=headers, timeout=3, verify=False)
        elif request.method == "POST":
            data = request.form
            headers.pop("content-type", None)
            headers.pop("content-length", None)
            res = requests.post(url, params=params, data=data, headers=headers, timeout=3, verify=False)
        return res.text
    except Exception as e:
        return "See https://wiku30.xyz/ctf/wiku_flag.py for hints."

@app.route("/", methods=["POST", "GET"])
def show():
    url = request.args.get('url', "")
    if url != "https://wiku30.xyz/":
        return "See https://wiku30.xyz/ctf/wiku_flag.py for hints.", 200

    res = proxy(url, request)
    if res == THE_ID:
        return FLAG, 200
    else:
        return "See https://wiku30.xyz/ctf/wiku_flag.py for hints.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="468")
