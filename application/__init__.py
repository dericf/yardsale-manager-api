#
# Configuration Object
#
from instance.config import CONFIG as conf
CONFIG = conf()
from sendgrid import SendGridAPIClient
sg_client = SendGridAPIClient(CONFIG.SEND_GRID_API_KEY)

from application.auth import auth_blueprint
from application.market import market_blueprint
from application.maps import maps_blueprint
#
# Flask
#
from flask import Flask, request, url_for, redirect
from flask_cors import CORS, cross_origin
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
# Create the flask application object
#
app = Flask(__name__, static_folder='application/static')
#
# Load the CONFIG object into the flask.app.config
#
app.config.from_object(CONFIG)
#
# Load blueprints
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(market_blueprint, url_prefix="/api/market")
app.register_blueprint(maps_blueprint, url_prefix="/api/maps")
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
