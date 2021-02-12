
from sendgrid.helpers.mail import Mail
import json
from instance.config import CONFIG as conf

from pprint import pprint
CONFIG = conf()

import logging

from application import sg_client

def send_email(from_email, to_emails, subject, html_content):
    email = Mail(from_email=from_email,
                   to_emails=to_emails,
                   subject=subject,
                   html_content=html_content)
    print('Message: ', email)

    try:
        print("\n\n\nsg: ", sg_client.__dict__)
        try:
            response = sg_client.send(email)
            # logging.info(response.status_code)
            # logging.info(response.body)
            # logging.info(response.headers)
        except Exception as e:
            print('Error sending email', e)
            raise Exception("COULD NOT SEND EMAIL")
        return True
    except Exception as e:
        print("Error connecting to SG", e )
        return None
