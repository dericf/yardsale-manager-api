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
from application.gql.mutations import CREATE_USER
from application.gql.queries import GET_USER_BY_EMAIL


def get_user_by_email(email):
    # TODO: get actual user here from the DB
    # user = {
    #     'uuid': '0012934747174924',
    #     'email':'test@test.com',
    #     'password':"$2b$12$JiR4ndNoEECgkoMzMn97U.MEBK5AMono3pPY47IaT1bzMDimkbmqu",
    #     'role': 'user'
    # }
    user = Query(GET_USER_BY_EMAIL, variables={"email": email}, as_admin=True)
    print('Getting User: ', user, email)

    if user['user'] == []:
        return None
    else:
        return user['user'][0]
