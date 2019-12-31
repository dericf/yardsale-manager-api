from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
from instance.config import CONFIG as conf
CONFIG = conf()

import logging

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
        logging.error("Error Sending Email", e.message)


def build_message(user_id, confirmation_key):
    subject = 'Email Confirmation Required'
    if CONFIG.ENV == 'dev':
        link = f'{CONFIG.HOST_BASE_URL}/auth/register/confirm?key={confirmation_key}&uid={user_id}'
        html_content = f'''<a type="button" href="{link}">{link}<a>'''
    else:
        link = f'{CONFIG.HOST_BASE_URL}/auth/register/confirm?key={confirmation_key}&uid={user_id}'
        html_content = f'''Click the link below to confirm your email. <br/> 
<a type="button" href="{link}">Confirm Email</a> <br />
or paste the following link into your browser <br />
{link}'''
    return subject, html_content


def send_confirmation_email(user):
    subject, html_content = build_message(user['uuid'], user['confirmation_key'])
    send_email(to_emails=user["email"], subject=subject, html_content=html_content)