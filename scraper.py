import requests
import time
import smtplib
import os
import sys

import logger

from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

# General globals
GAME = 'BL3' # BL2, BL3
SHIFT_CODES_URL = 'https://shift.orcicorn.com/shift-code/'
REWARDS_URL = 'https://shift.gearboxsoftware.com/rewards'
FILE = '{}_shift_codes.txt'.format(GAME)
LOGGER = logger.get_logger(os.path.basename(__file__))

# SMTP globals
SMTP_PORT = 465
SMTP_SERVER = os.environ['SMTP_SERVER']
SMTP_USER = os.environ['SMTP_USER']
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']
RECIPIENTS = os.environ['SHIFT_CODE_RECIPIENTS'] # Email addresses, semicolon delimited


def get_new_codes():
    """Scrapes SHIFT_CODES_URL to see if new codes are available.

    Returns:
        list: A list of new codes. Empty if no codes are found.
    """
    new_codes = []
    today = str(datetime.now().strftime('%d %b %Y')).upper()

    # Load existing SHIFT codes
    # Create the file if it doesn't exist
    if not os.path.exists(FILE):
        with open(FILE, 'w+') as f:
            shift_codes = []
    else:
        with open(FILE, 'r') as f:
            shift_codes = f.read().split('\n')

    # Parse the SHIFT_CODES_URL page for archive-item articles
    response = requests.get(SHIFT_CODES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.findAll('article', {'class': 'archive-item'})

    for item in items:
        # Parse each article for the SHIFT code, game and date
        code = item.find('a', {'class': 'archive-item-link'}).contents[0].strip()
        game = item.find('a', {'class': 'archive-item-link'}).contents[1].contents[0]
        date = item.find('span', {'class': 'archive-item-date'}).contents[0]

        if GAME in game and code not in shift_codes and today in date:
            # We found a new code if we made it here
            # Append to our FILE and new_codes list
            LOGGER.info('New code found: {}'.format(code))
            with open(FILE, 'a') as f:
                f.write('{}\n'.format(code))
            new_codes.append(code)

    return new_codes


def send_codes_via_email(codes):
    """Sends an email if new codes are found.

    Args:
        codes (list): A list of codes. Returns if empty.
    """
    if not codes:
        LOGGER.info('No new codes found.')
        return

    LOGGER.info('Sending new codes to: {}'.format(RECIPIENTS))
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASSWORD)
    
    body = '<html><head></head><body><p>{}<br><br>{}</p></body></html>'.format(
        '\n'.join(codes),
        REWARDS_URL
    )

    for recipient in RECIPIENTS.split(';'):
        msg = MIMEText(body, 'html')
        msg['Subject'] = '{} Shift Codes'.format(GAME)
        msg['From'] = SMTP_USER
        msg['To'] = recipient
        server.sendmail(SMTP_USER, recipient, msg.as_string())


if __name__ == '__main__':
    # Infinite loop to check for codes
    # Sleep for one hour between checks
    while True:
        # Send codes if we found any
        send_codes_via_email(get_new_codes())

        # Sleep for 1 hour
        LOGGER.info('Sleeping for one hour.')
        time.sleep(3600)
