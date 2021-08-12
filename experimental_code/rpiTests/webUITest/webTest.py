from flask import Flask
from flask import request

import time

webApp = Flask(__name__)

@app.route("/")
def web_interface():
    html = open("webTest.html")
    response = html.read().replace('\n', '')
    html.close()
    return response

