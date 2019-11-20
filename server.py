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


def send_email(to_emails, subject, html_content):
    message = Mail(from_email=CONFIG.SEND_GRID_FROM_EMAIL,
                   to_emails=to_emails,
                   subject=subject,
                   html_content=html_content)

    try:
        sg = SendGridAPIClient(CONFIG.SEND_GRID_API_KEY)
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)
    except Exception as e:
        logging.error("Error", e.message)


def get_user_by_email(email):
    # TODO: get actual user here from the DB
    user = {
        'uuid': '0012934747174924',
        'email':'test@test.com',
        'password':"$2b$12$JiR4ndNoEECgkoMzMn97U.MEBK5AMono3pPY47IaT1bzMDimkbmqu",
        'role': 'user'
    }
    return user


def generate_auth_token(user):
    payload = {
        "uuid": user['uuid'],
        "email": user['email'],
        "role": user['role'],
        "exp": f'{datetime.datetime.utcnow() + datetime.timedelta(seconds=900)}'
    }
    token = jwt.encode(payload, app.config.get(
        'SECRET_KEY'), algorithm='HS256')

    print(token)

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
        if  bcrypt.checkpw(password.encode('utf8'), try_user['password'].encode('utf8')):
            #
            # Success!
            #
            token = generate_auth_token(try_user)
            return {"STATUS": "OK", "token": token}
        else:
            return {"STATUS": "ERROR", "MESSAGE": "Incorrect password. Please try again."}


def is_email_valid_to_register(email):
    # TODO: Implement Logic here
    return True


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
    # TODO
    # Hash password
    pwd_hash = generate_password_hash(password)
    print(pwd_hash)
    pass


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

    # TODO: Add actual logic here
    # Check if username is valid (does not already exist in DB and is the correct length/format etc)
    if is_email_valid_to_register(email) and is_valid_password(password) and password == confirm_password:
        # if yes:
        #           - generate random confirmation key and store in DB
        #           - send registration confirmation email
        #
        key = generate_random_confirmation_key()
        register_new_user(email, password, key)
        return {"STATUS": "OK", "MESSAGE": "Success! Please check your email for the confirmation link."}
    else:
        # if no: return {"STATUS": "ERROR", "MESSAGE": "Username already exists"}
        return {"STATUS": "ERROR", "MESSAGE": "An account with that email already exists. Please try again."}


@app.route('/auth/register/confirm', methods=['GET'])
def auth_register_confirm():
    confirmation_key = request.args.get('key')
    username = request.args.get('username')
    # TODO: Add actual logic here
    # compare the conf key and username and make sure they match the record in the DB
    return {"STATUS": "OK"}


if __name__ == '__main__':
    try:
        os.mkdir(CONFIG.UPLOAD_FOLDER)
    except:
        pass
    app.run(host=CONFIG.SERVER_HOST, port=CONFIG.SERVER_PORT)
