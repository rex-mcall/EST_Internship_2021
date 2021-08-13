from flask import Flask
from flask import request
import sqlite3

import time

webApp = Flask(__name__)

@webApp.route("/")
def web_interface():
    html = open("experimental_code\\rpiTests\\webUITest\\webTest.html")
    response = html.read().replace('\n', '')
    html.close()
    return response

def main():
    webApp.run(host= "0.0.0.0")

main()