#
# Flask
#
from . import auth_blueprint
from flask import Flask, request, url_for, redirect, Response, make_response
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
from application.auth.user import get_user_by_email, get_user_by_uuid

CONFIG = conf()


def generate_auth_token(user):
    '''Generates a JWT access token.
    '''
    payload = {
        "email": user['email'],
        "aud": CONFIG.JWT_AUDIENCE,
        "exp": (datetime.datetime.utcnow() + datetime.timedelta(seconds=CONFIG.ACCESS_TOKEN_EXPIRE)),
        "alg": "RS256",
        "expires_at": "",
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

    # print(token.decode('UTF-8'))

    return token.decode('UTF-8')


def generate_refresh_token(user):
    '''Generates a JWT refresh token.
    '''
    payload = {
        "email": user['email'],
        "aud": CONFIG.JWT_AUDIENCE,
        "exp": (datetime.datetime.utcnow() + datetime.timedelta(seconds=CONFIG.REFRESH_TOKEN_EXPIRE)),
        "expires_at": "",
        "alg": "RS256",
        "token_version": 0
    }
    token = jwt.encode(payload, CONFIG.JWT_SECRET, algorithm='RS256')

    # print(token)

    # print(token.decode('UTF-8'))

    return token.decode('UTF-8')


@auth_blueprint.route('/login', methods=['POST'])
def auth_login():
    '''Login: The user tries to log in by posting via the client with data in the body of the request.
    If the username and password match the DB record, then a token will be generated and sent back in the response.
    This token expires based on CONFIG.ACCESS_TOKEN_EXPIRE.
    If either username does not exist or username/password combo do not match, then return an error with the appropriate message.
    '''
    # Get request body as json(dict)
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    #
    # Check the credentials (Try and get a user with that email)
    #
    user = get_user_by_email(email)
    if user is None:  # user does not exist based on that email
        return {
            "STATUS": "ERROR",
            "MESSAGE": "User not found"
        }
    else:
        if bcrypt.checkpw(password.encode('utf8'), user['password_hash'].encode('utf8')):
            #
            # User credentials are correct!
            #
            if not user['has_confirmed']:
                #
                # User has not confirmed their email yet
                #
                return {
                    "STATUS": "ERROR",
                    "MESSAGE": "Email not confirmed"
                }

            token = generate_auth_token(user)
            refresh_token = generate_refresh_token(user)
            res = make_response(
                {
                    "STATUS": "OK",
                    "token": token,
                    "tokenExpiry": CONFIG.ACCESS_TOKEN_EXPIRE,
                    "refreshToken": refresh_token,
                    "callback": f"http://127.0.0.1:8000/auth/callback?uuid={user['uuid']}",
                    "user": {
                        "uuid": user['uuid'],
                        "email": user['email'],
                        "name": user['name'],
                        "initials": user['initials'],
                        "hasCompletedOnboarding": user['has_completed_onboarding']
                    }
                }
            )
            # res.headers['Access-Control-Allow-Credentials'] = True
            # res.set_cookie(key='refreshToken', value=refresh_token,
            #                domain='127.0.0.1:3000', httponly=True)  # max_age=CONFIG.REFRESH_TOKEN_EXPIRE,
            return res
        else:
            return {"STATUS": "ERROR", "MESSAGE": "Wrong password"}


@auth_blueprint.route('/callback')
def login_callback():
    """
    This should set a cookie on the client containing a valid jwt
    """
    user = get_user_by_uuid(request.args.get('uuid'))
    # print('\n\n\nCALLBACK USER: ', user)
    if user:
        refresh_token = generate_refresh_token(user)
        res = make_response(
            {"STATUS": "OK", "refreshToken": refresh_token})
        res.headers['Access-Control-Allow-Credentials'] = True
        res.set_cookie(key='refreshToken', value=refresh_token,
                       domain='127.0.0.1', httponly=True)  # max_age=CONFIG.REFRESH_TOKEN_EXPIRE,
        return res


@auth_blueprint.route('/refresh', methods=['POST'])
def auth_refresh():
    # TODO: Refresh token here
    print('Request Cookies: ', request.cookies)
    body = request.get_json()
    print('Body: ', body)
    #
    # TODO: Decode refresh token and get user
    #
    try:
        rt = body.get('refreshToken')
        print('\n\nRT: ', rt)
        decoded_result = decode_token(rt, verify=True)
        print('Refresh Token Result: ', decoded_result)
        # user = get_user_by_email(refresh['email'])
        # print('User from RF Token: ', user)
        # new_token = generate_auth_token(user)
        if decoded_result[0] == 'ERROR' and decoded_result[1] == "EXPIRED":
            return {"STATUS": "ERROR", 'MESSAGE': "refresh token expired", "newToken": None}
        elif decoded_result[0] == 'SUCCESS' and decoded_result[1] == 'VALID':
            user = get_user_by_email(decoded_result[2]['email'])
            returnUser = {
                "uuid": user['uuid'],
                "email": user['email'],
                "name": user['name'],
                "initials": user['initials'],
                "hasCompletedOnboarding": user['has_completed_onboarding']
            }
            return {"STATUS": "OK", "newToken": generate_auth_token(user), "user": returnUser, "newRefreshToken": generate_refresh_token(user)}
    except Exception as e:
        print('\n\n\n\nError: ', str(e))
        return {'STATUS': "ERROR"}
    #
    # TODO: Generate new access token
    #


def decode_token(raw_token, verify=False):
    try:
        decoded = jwt.decode(raw_token, CONFIG.JWT_PUBLIC_KEY, algorithms=[
                             'RS256'], audience=CONFIG.JWT_AUDIENCE, verify=verify)
        return ('SUCCESS', 'VALID', decoded)
    except jwt.ExpiredSignatureError as e:
        print('INVALID TOKEN: EXPIRED!')
        return ('ERROR', 'EXPIRED', None)
