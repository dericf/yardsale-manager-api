#
# Flask
#
from . import market_blueprint
from flask import Flask, request, url_for, redirect, render_template_string
from flask_cors import CORS, cross_origin
#
# Configuration Object
#
from config import CONFIG as conf
#
# Python Standard Library
#
import logging
import os
from pprint import pprint
import json
from time import gmtime, strftime
import datetime
import uuid
#
# GraphQL
#
from application.gql import Query, Mutation
from application.gql.mutations import CREATE_USER, CREATE_SELLER
from application.gql.queries import GET_PUBLIC_YARDSALES
#
# SendGrid Library
#
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
#
# Email Helper Functions
#
from application.send_grid.register import send_confirmation_email


@market_blueprint.route('/get-all-public-yardsales/<string:lat>/<string:lng>')
def get_public_yardsales_for_location(lat, lng):
    yardsales = Query(GET_PUBLIC_YARDSALES, as_admin=True)
    if yardsales:
        return {"yardsales": yardsales["yardsale"]}
    else:
        return {"yardsales": []}

@market_blueprint.route('/get-all-filtered-yardsales/<string:city>')
def get_public_yardsales_for_city(city):
    city = str(city).lower()
    yardsales = Query(GET_PUBLIC_YARDSALES, as_admin=True)
    if yardsales:
        return {"yardsales": yardsales["yardsale"]}
    else:
        return {"yardsales": []}