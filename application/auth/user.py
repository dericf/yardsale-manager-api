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
import uuid as uuidlib
#
# Password Hashing
#
import bcrypt
#
# GraphQL
#
from application.gql import Query, Mutation
from application.gql.mutations import CREATE_USER, SET_USER_EMAIL_CONFIRMED, SET_PASSWORD_RESET_CODE, UPDATE_PASSWORD
from application.gql.queries import GET_USER_BY_EMAIL, GET_USER_BY_UUID


def get_user_by_email(email):
    #
    # Make a GQL Call as an admin
    #
    try:
        user = Query(GET_USER_BY_EMAIL, variables={
                     "email": email}, as_admin=True)
        if user['user'] == []:
            return None
        else:
            return user['user'][0]
    except Exception as e:
        print('There was an error with the GraphQL Query...')
        print(str(e))
        return None


def get_user_by_uuid(uuid):
    #
    # Make a GQL Call as an admin
    #
    user = Query(GET_USER_BY_UUID, variables={"uuid": uuid}, as_admin=True)

    if user['user'] == []:
        return None
    else:
        return user['user'][0]


def generate_password_hash(password):
    # return bcrypt.kdf(
    #     password=password,
    #     salt=CONFIG.BCRYPT_SALT,
    #     desired_key_bytes=32,
    #     rounds=100
    # )
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def confirm_user(uuid):
    user = Mutation(SET_USER_EMAIL_CONFIRMED, {"uuid": uuid}, as_admin=True)

    if 'data' in user:
        return user['data']['update_user']['returning'][0]
    else:
        return None


def generate_and_set_password_reset_code(uuid):
    reset_code = str(uuidlib.uuid4())
    # print("reset code: ", reset_code)
    Mutation(SET_PASSWORD_RESET_CODE, variables={
        "uuid": uuid,
        "code": reset_code
    }, as_admin=True)

    return reset_code


def set_new_password(user_uuid, new_password):
    new_password_hash = generate_password_hash(new_password)
    variables = {
        "uuid": user_uuid,
        "password": str(new_password_hash, encoding="UTF-8")
    }
    result = Mutation(UPDATE_PASSWORD, variables, as_admin=True)
    # print('RESULT: ', result)
