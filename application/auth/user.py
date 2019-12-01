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
# GraphQL
#
from application.gql import Query, Mutation
from application.gql.mutations import CREATE_USER, SET_USER_EMAIL_CONFIRMED
from application.gql.queries import GET_USER_BY_EMAIL, GET_USER_BY_UUID


def get_user_by_email(email):
    #
    # Make a GQL Call as an admin
    #
    user = Query(GET_USER_BY_EMAIL, variables={"email": email}, as_admin=True)
    # print('Getting User: ', user, email)

    if user['user'] == []:
        return None
    else:
        return user['user'][0]


def get_user_by_uuid(uuid):
    #
    # Make a GQL Call as an admin
    #
    print('\n\n\n UUID: ', uuid)
    user = Query(GET_USER_BY_UUID, variables={"uuid": uuid}, as_admin=True)
    print('\n\n\n\n\nUser: ', user)
    if user['user'] == []:
        return None
    else:
        return user['user'][0]


def confirm_user(uuid):
    user = Mutation(SET_USER_EMAIL_CONFIRMED, {"uuid": uuid}, as_admin=True)

    if 'data' in user:
        return user['data']['update_user']['returning'][0]
    else:
        return None
