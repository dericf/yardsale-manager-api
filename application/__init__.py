#
# Flask
#
from application.auth import auth_blueprint
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

# TODO:
# sudo apt-get install build-essential libffi-dev python-dev

#
# Instantiate the configuration object
#
CONFIG = conf()
#
# Create the flask application object
#
app = Flask(__name__)
#
# Load the CONFIG object into the flask.app.config
#
app.config.from_object(CONFIG)
#
# Load blueprints
app.register_blueprint(auth_blueprint, url_prefix="/auth")
#
#
# Initialize CORS
#
cors = CORS(
    app,
    support_credentials=True,
    resources={
        # Accept all url patterns
        r"/*": {"origins": CONFIG.CLIENT_ORIGINS}
    }
)
#
# Initialize Server Loging
#
logging.basicConfig(level="INFO", filename='app.log', filemode='a',
                    format="%(asctime)s - %(process)d - %(levelname)s - %(message)s", datefmt="%a, %d %b %Y %H:%M:%S")


@app.route('/')
def index():
    logging.info('Hit the index route...')
    return {"API_STATUS": "OK"}


@app.errorhandler(500)
def server_error(e):
    # logging.exception('An error occurred during a request. %s', e)
    return "An internal error occurred", 500
