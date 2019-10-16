# BL3_SHIFT_Code_Scraper
Scrape BL3 SHIFT codes every hour and send any new found codes to email recipients.

## Requirements
*BeautifulSoup 4*: `pip install beautifulsoup4`

## Setup
The following environment variables must exist:

`SMTP_SERVER`: The SMTP server name

`SMTP_USER`: The username used to authenticate with the SMTP server

`SMTP_PASSWORD`: The password used to authenticate with the SMTP server

`SHIFT_CODE_RECIPIENTS`: Email addresses, semicolon delimited

## Run
Once the afformentioned environment variables exist, simply run the script: `python3 scraper.py`
