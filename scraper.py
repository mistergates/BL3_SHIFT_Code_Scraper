import requests
import time
import smtplib
import os
import logging
from datetime import datetime
from bs4 import BeautifulSoup

GAME = 'BL3' # BL2, BL3
SHIFT_CODES_URL = 'https://shift.orcicorn.com/shift-code/'
REWARDS_URL = 'https://shift.gearboxsoftware.com/rewards'
FILE = '{}_shift_codes.txt'.format(GAME)

SMTP_PORT = 465
SMTP_SERVER = os.environ['SMTP_SERVER']
SMTP_USER = os.environ['SMTP_USER']
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']
RECIPIENTS = os.environ['SHIFT_CODE_RECIPIENTS'] # Email addresses, semicolon delimited

if __name__ == '__main__':
    while True:
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
                logging.info('New code found: {}'.format(code))
                with open(FILE, 'a') as f:
                    f.write('{}\n'.format(code))
                new_codes.append(code)

        if new_codes:
            # If we found new codes send an email
            logging.info('Sending new codes to: {}'.format(RECIPIENTS))
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            msg = '\r\n'.join(
                [
                    'From: {}'.format(SMTP_USER),
                    'To: {}'.format(RECIPIENTS),
                    'Subject: {} Shift Codes'.format(GAME),
                    '',
                    '{}'.format('\n'.join(new_codes)) + '\n\n{}'.format(REWARDS_URL)
                ]
            )
            server.sendmail(SMTP_USER, RECIPIENTS, msg)

        # Sleep for 1 hour
        time.sleep(3600)
