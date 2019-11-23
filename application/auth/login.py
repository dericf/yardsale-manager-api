#
# Flask
#
from . import auth_blueprint
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
#
# Password Hashing
#
import bcrypt
#
# JWT
#
import jwt
#
# GraphQL
#
from application.gql import Query, Mutation
from application.gql.mutations import CREATE_USER
from application.gql.queries import GET_USER_BY_EMAIL
#
# User Helper Functions
#
from application.auth.user import get_user_by_email

CONFIG = conf()

def generate_auth_token(user):
    payload = {
        "email": user['email'],
        "aud": "localhost:8000",
        "exp": (datetime.datetime.utcnow() + datetime.timedelta(seconds=900)),
        "alg": "RS256",
        "https://hasura.io/jwt/claims": {
            "x-hasura-allowed-roles": ["user"],
            "x-hasura-default-role": "anonymous",
            "x-hasura-user-id": user['uuid'],
            "x-hasura-org-id": "123",
            "x-hasura-role": user['role'],
            "x-hasura-custom": "custom-value"
        }
    }
    token = jwt.encode(payload, CONFIG.JWT_SECRET, algorithm='RS256')

    # print(token)

    print(token.decode('UTF-8'))

    return token.decode('UTF-8')


@auth_blueprint.route('/login', methods=['POST'])
def auth_login():
    '''Login: The user tries to log in by posting a form on the client.
    If the username and password match the DB record, then a token will be generated and sent back in the response.
    This token should expire.
    If either username does not exist or username/password combo do not match, then return an error with the appropriate message.
    '''
    data = request.get_json()
    # TODO: Add actual logic here
    email = data.get('email')
    password = data.get('password')
    #
    # Check the credentials
    #
    try_user = get_user_by_email(email)
    if try_user is None:  # user does not exist based on that email
        return {"STATUS": "ERROR", "MESSAGE": "User not found with that email"}
    else:
        if bcrypt.checkpw(password.encode('utf8'), try_user['password_hash'].encode('utf8')):
            #
            # Success!
            #
            token = generate_auth_token(try_user)
            return {"STATUS": "OK", "token": token}
        else:
            return {"STATUS": "ERROR", "MESSAGE": "Incorrect password. Please try again."}


@auth_blueprint.route('/refresh', methods=['POST'])
def auth_refresh():
    # TODO: Refresh token here
    pass


def decode_token(raw_token):
    return jwt.decode(raw_token, CONFIG.JWT_PUBLIC_KEY, algorithms=['RS256'], audience="localhost:8000")
