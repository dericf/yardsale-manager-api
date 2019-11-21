from flask import Flask, request, url_for, redirect

from instance.config import CONFIG as conf
from flask_cors import CORS, cross_origin
#
# SendGrid
#
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import logging
import os
from pprint import pprint
import json
from time import gmtime, strftime
import jwt
import datetime
import bcrypt

from application.gql import Query, Mutation
from application.gql.mutations import CREATE_USER
from application.gql.queries import GET_USER_BY_EMAIL

from application.send_grid.register import send_confirmation_email

# TODO:
# sudo apt-get install build-essential libffi-dev python-dev

import html

CONFIG = conf()

app = Flask(__name__)
app.config.from_object(CONFIG)
cors = CORS(
    app,
    resources={
        # TODO: Add a specific origin
        r"/*": {"origins": CONFIG.CLIENT_ORIGINS}
    }
)

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


def get_user_by_email(email):
    # TODO: get actual user here from the DB
    # user = {
    #     'uuid': '0012934747174924',
    #     'email':'test@test.com',
    #     'password':"$2b$12$JiR4ndNoEECgkoMzMn97U.MEBK5AMono3pPY47IaT1bzMDimkbmqu",
    #     'role': 'user'
    # }
    user = Query(GET_USER_BY_EMAIL, variables={"email": email}, as_admin=True)
    # print('Getting User: ', user['user'])
    if user['user'] == []:
        return None
    else:
        return user['user'][0]


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


@app.route('/auth/login', methods=['POST'])
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


def is_email_valid_to_register(email):
    # TODO: Implement Logic here
    if "@" not in email or "." not in email:
        return False
    user = get_user_by_email(email)
    if user is None:
        return True
    else:
        return False


def generate_random_confirmation_key():
    # TODO
    return 'asdasd'


def save_confirmation_key(key, user):
    # TODO
    pass


def generate_password_hash(password):
    # return bcrypt.kdf(
    #     password=password,
    #     salt=CONFIG.BCRYPT_SALT,
    #     desired_key_bytes=32,
    #     rounds=100
    # )
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def register_new_user(email, password, confirmation_key):
    # Hash password
    pwd_hash = generate_password_hash(password)
    print(pwd_hash)
    variables = {
        "email": email,
        "passwordHash": str(pwd_hash, encoding="UTF-8"),
        "confirmationKey": confirmation_key
    }
    new_user = Mutation(mutation=CREATE_USER,
                        variables=variables, as_admin=True)
    if 'data' in new_user:
        return new_user['data']['insert_user']['returning'][0]
    else:
        return None


def is_valid_password(password):
    if password is not None and password != '':
        if len(password) >= 4:
            return True
    return False


@app.route('/auth/register', methods=['POST'])
def auth_register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Check if username is valid (does not already exist in DB and is the correct length/format etc)
    if is_email_valid_to_register(email) and is_valid_password(password) and password == confirm_password:
        # if yes:
        #           - generate random confirmation key and store in DB
        #           - send registration confirmation email
        #
        key = generate_random_confirmation_key()
        new_user = register_new_user(email, password, key)
        print('New User is: ', new_user)
        send_confirmation_email(user=new_user)
        return {"STATUS": "OK", "MESSAGE": "Success! Please check your email for the confirmation link."}
    else:
        # if no: return {"STATUS": "ERROR", "MESSAGE": "Username already exists"}
        return {"STATUS": "ERROR", "MESSAGE": "An account with that email already exists. Please try again."}


@app.route('/auth/register/confirm', methods=['GET'])
def auth_register_confirm():
    confirmation_key = request.args.get('key')
    uid = request.args.get('uid')
    # print('Confirmation for ')
    # TODO: Add actual logic here
    # compare the conf key and username and make sure they match the record in the DB
    return {"STATUS": "OK"}


@app.route('/auth/refresh', methods={'POST'})
def auth_refresh():
    # TODO: Refresh token here
    pass


def decode_token(raw_token):
    return jwt.decode(raw_token, CONFIG.JWT_PUBLIC_KEY, algorithms=['RS256'], audience="localhost:8000")


if __name__ == '__main__':
    try:
        os.mkdir(CONFIG.UPLOAD_FOLDER)
    except:
        pass
    app.run(host=CONFIG.SERVER_HOST, port=CONFIG.SERVER_PORT)
