#
# Flask
#
from . import auth_blueprint
from flask import Flask, request, url_for, redirect, render_template_string
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
import uuid as uuidlib
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
from application.gql.mutations import CREATE_USER, CREATE_SELLER
from application.gql.queries import GET_USER_BY_EMAIL
#
# User Helper Functions
#
from application.auth.user import get_user_by_email, get_user_by_uuid, confirm_user, generate_password_hash
#
# SendGrid Library
#
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
#
# Email Helper Functions
#
from application.send_grid.register import send_confirmation_email



CONFIG = conf()

def is_email_valid_to_register(email):
    # TODO: Implement Logic here
    if "@" not in email or "." not in email:
        return False
    user = get_user_by_email(email)
    if user is None:
        return True
    else:
        return False


def generate_random_uuid():
    # Generate a UUID as a confirmation key
    return str(uuidlib.uuid4())


def save_confirmation_key(key, user):
    # TODO
    pass

def register_new_user(name, initials, email, password, confirmation_key):
    # Hash password
    pwd_hash = generate_password_hash(password)
    variables = {
        "name": name,
        "initials": initials,
        "email": email,
        "passwordHash": str(pwd_hash, encoding="UTF-8"),
        "confirmationKey": confirmation_key
    }
    new_user = Mutation(mutation=CREATE_USER,
                        variables=variables, as_admin=True)
    #
    # Now create new seller for this user (that way the user can itsself be used as a seller on a yardsale)
    #
    if 'data' in new_user:
        return new_user['data']['insert_user']['returning'][0]
    else:
        return None


def is_valid_password(password):
    if password is not None and password != '':
        if len(password) >= 4:
            return True
    return False


def create_seller_for_new_user(user):
    variables = {
        "user_uuid": user['uuid'],
        "name": user['name'],
        "initials": user['initials'],
        "email": user['email']
    }
    new_seller = Mutation(mutation=CREATE_SELLER,
                          variables=variables, as_admin=True)


@auth_blueprint.route('/register', methods=['POST'])
def auth_register():
    data = request.get_json()
    name = data.get('name')
    initials = data.get('initials')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    # print('POST DATA: ', data)
    # Check if username is valid (does not already exist in DB and is the correct length/format etc)
    if is_email_valid_to_register(email) and is_valid_password(password) and password == confirm_password:
        # if yes:
        #           - generate random confirmation key and store in DB
        #           - send registration confirmation email
        #
        key = generate_random_uuid()
        #
        new_user = register_new_user(name, initials, email, password, key)
        #
        create_seller_for_new_user(user=new_user)
        #
        # Todo: send this off to a redis queue
        #
        send_confirmation_email(user=new_user)
        #
        return {"STATUS": "OK", "MESSAGE": "Success! Please check your email for the confirmation link."}
    else:
        # if no: return {"STATUS": "ERROR", "MESSAGE": "Username already exists"}
        return {"STATUS": "ERROR", "MESSAGE": "An account with that email already exists. Please try again."}


@auth_blueprint.route('/register/confirm', methods=['GET'])
def auth_register_confirm():
    confirmation_key = request.args.get('key')
    uid = request.args.get('uid')

    user = get_user_by_uuid(uid)
    # print('User: ', user)
    if user['confirmation_key'] == confirmation_key:
        # This was the correct link. Proceed to confirm
        #
        user = confirm_user(uid)
        # return {"STATUS": "OK", "MESSAGE": "User has been confirmed. You may now log in at https://yardsalemanager.meqsoftware.com/login"}
        return {"STATUS": "OK"} # redirect(f"{CONFIG.CLIENT_BASE_URL}/register/confirm-email")
    else:
        return {"STATUS": "ERROR", "MESSAGE": "Something went wrong. The link provided might have been changed from the original."}
