from flask import request, render_template, render_template_string
from . import auth_blueprint
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
# Password Hashing
#
import bcrypt
#
# GraphQL
#
from application.gql import Query, Mutation
from application.gql.mutations import CREATE_USER, SET_USER_EMAIL_CONFIRMED
from application.gql.queries import GET_USER_BY_EMAIL, GET_USER_BY_UUID
#
# Emails
#
from application.send_grid import send_email

from application.auth.user import get_user_by_email, get_user_by_uuid, generate_and_set_password_reset_code, set_new_password

CONFIG = conf()

# Request a change of password
#   - set the DB flag
#   - generate a random reset code
#   - format a link with that code (yardsalemanager.com/reset-password?code=F2A993gSCm249cCJa)
#       - This code will get placed in the form when submitting for a new password and will be
#           checked on the server when submitting the for with the new password
@auth_blueprint.route('/request-change-password', methods=["POST"])
def request_password_change():
    body = request.get_json()
    # Expected fields:
    # body.email
    if not body.get('email'):
        return {"STATUS": "ERROR",  "MESSAGE": "User not found"}
    # Check if email is valid for a user
    user = get_user_by_email(body.get("email"))
    if not user:
        return {"STATUS": "ERROR",  "MESSAGE": "User not found"}
    reset_code = generate_and_set_password_reset_code(user["uuid"])
    try:
        send_reset_email(user, reset_code)
        return {"STATUS": "OK"}
    except Exception as e:
        return {"STATUS": "ERROR", "MESSAGE": "Something went wrong when sending the email. Please try again", "ERROR": f"{e}"}

#
# Build the Reset Password Link
#
def get_reset_password_link(user, reset_code):
    return f"{CONFIG.CLIENT_BASE_URL}/confirm-change-password?resetCode={reset_code}&uuid={user['uuid']}"

#
# Send reset email
#
def send_reset_email(user, reset_code):

    # 'password-recovery@yardsalemanager.com'
    from_email = 'password-recovery@yardsalemanger.com'
    to_email = user["email"]
    subject = 'Password Reset'
    reset_link = get_reset_password_link(user, reset_code)
    body = render_template('reset-password.html', user=user, reset_link=reset_link)
    # body = f'''Click the link below to set a new password for your yardsalemanager.com account.
    # <a href="">Reset Password</a>'''
    send_email(from_email=from_email, to_emails=to_email,
               subject=subject, html_content=body)


# Handle POST from '/reset-password' with the new password and the reset code
#   - Must check the the reset-code matches the user record in the DB. This means they
#       did indeed come from the link in the email (that is the only place that code exists)
@auth_blueprint.route('/complete-change-password', methods=['POST'])
def complete_set_new_password():
    body = request.get_json()

    reset_code = body.get("reset_code")
    uuid = body.get("uuid")
    new_password = body.get("new_password")
    confirm_new_password = body.get("confirm_new_password")

    # body.email, new_password, confirm_new_password, reset_code
    if not uuid or not reset_code:
        return {"STATUS": "ERROR", "MESSAGE": "Bad/Missing Values"}

    # Double check the user is valid
    user = get_user_by_uuid(uuid)
    if not user:
        return {"STATUS": "ERROR", "MESSAGE": "User not found"}

    if reset_code != user['password_reset_code']:
        return {"STATUS": "ERROR", "MESSAGE": "Reset code does not match"}

    if new_password != confirm_new_password:
        return {"STATUS": "ERROR", "MESSAGE": "Passwords do not match"}

    set_new_password(uuid, new_password)

    return {"STATUS": "OK"}

# Handle POST from '/reset-password' with the new password and the reset code
#   - Must check the the reset-code matches the user record in the DB. This means they
#       did indeed come from the link in the email (that is the only place that code exists)
@auth_blueprint.route('/authenticated-change-password', methods=['POST'])
def change_password_while_authenticated():
    body = request.get_json()

    user_uuid = body.get("userUUID")
    current_password = body.get("currentPassword")
    new_password = body.get("newPassword")
    confirm_new_password = body.get("confirmNewPassword")

    # Double check the user is valid
    user = get_user_by_uuid(user_uuid)
    if not user:
        return {"STATUS": "ERROR", "MESSAGE": "Something went wrong with the request. Please refresh the page and try again."}

    if not bcrypt.checkpw(current_password.encode('utf8'), user['password_hash'].encode('utf8')):
        return {"STATUS": "ERROR", "MESSAGE": "The current password you entered does not match our records."}

    if new_password != confirm_new_password:
        return {"STATUS": "ERROR", "MESSAGE": "Passwords do not match"}
    
    if new_password == current_password:
        return {"STATUS": "ERROR", "MESSAGE": "New password cannot be the same as your current password."}

    set_new_password(user_uuid, new_password)
    return {
        "STATUS": "OK", "MESSAGE": "Your Password has been changed."
    }