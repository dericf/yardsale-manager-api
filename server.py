#
# Flask
#
from flask import Flask, request, url_for, redirect
from flask_cors import CORS, cross_origin
#
# Configuration Object
#
from instance.config import CONFIG as conf
#
# Python Standard Library
#
import logging
import os
from pprint import pprint
import json
from time import gmtime, strftime
import datetime

from application import app

CONFIG = conf()

def create_directories():
    try:
        os.mkdir(CONFIG.UPLOAD_FOLDER)
    except:
        pass


def init_server():
    create_directories()


from application.auth import login, register, user

if __name__ == '__main__':
    init_server()
    app.run(host=CONFIG.SERVER_HOST, port=CONFIG.SERVER_PORT)
