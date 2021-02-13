import logging
from flask import render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
from config import CONFIG as conf
CONFIG = conf()


def send_email(to_emails, subject, html_content):
    #
    # Build Sendgrid Mail Object
    #
    message = Mail(from_email='welcome@yardsalemanager.com',
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


def send_confirmation_email(user):
    subject = 'Email Confirmation Required'
    #
    # Build the confirm link
    #
    confirm_link = f"{CONFIG.HOST_BASE_URL}/auth/register/confirm?key={user['confirmation_key']}&uid={user['uuid']}"
    #
    # Render the HTML email template
    #
    html_content = render_template(
        'register-confirm-email.html', user=user, confirm_link=confirm_link)
    #
    # Send the email
    #
    send_email(to_emails=user["email"],
               subject=subject, html_content=html_content)
