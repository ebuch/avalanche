import os
import re
import csv
import sys
import time
import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# /////////////////////////////////////////////
# // Setup: Please enter the following info. //
# /////////////////////////////////////////////

# Set the artist name and artist ID.
# Artist Name does not need to be precise. It is simply used for separating reports for different artists into different folders on your PC.
# Artist ID can be found in the URL bar of your browser when logged into your Materia Dashboard account.

artist_name = "Artist Name"
artist_id = 000

# Set authentication credentials

login_email = "EMAIL"
login_password = "PASSWORD"

# Once you've set up the above parameters, you're ready to go! Run download_reports.py

# //////////////////////////////////
# // Don't change anything below. //
# //////////////////////////////////

# Set the download date
date_downloaded = datetime.datetime.now().strftime("%Y%m%d")

# Start a browser session
driver = webdriver.Chrome()

# Navigate to the login page
driver.get(f"https://dash.materiamusic.com/artist/{artist_id}/reports")

wait = WebDriverWait(driver, 5)

# Find the username and password fields and enter your login information
username_field = driver.find_element(By.ID, "username")
username_field.send_keys(login_email)
username_field.send_keys(Keys.RETURN)

password_field = driver.find_element(By.ID, "password")
password_field.send_keys(login_password)
password_field.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(5)

# Check if the login attempt was unsuccessful
if "login" in driver.current_url:
    print("Login attempt unsuccessful. Please check your login credentials and try again.")
    driver.quit()
    sys.exit()

# extract the cookies as a dictionary
cookies = driver.get_cookies()
auth_cookie = next(cookie for cookie in cookies if cookie['name'] == 'materiacollective')['value']

# set the cookie as a dictionary
cookie = {
    'materiacollective': auth_cookie
}

# get page source using Selenium
page_source = driver.page_source

# create BeautifulSoup object
soup = BeautifulSoup(page_source, 'html.parser')

# define the directory paths
base_path = f"{artist_name}/"
date_path = os.path.join(base_path, date_downloaded)
individual_reports_path = os.path.join(date_path, "Individual Reports")

# check if the directories exist and create them if they don't
if not os.path.exists(base_path):
    os.makedirs(base_path)
if not os.path.exists(date_path):
    os.makedirs(date_path)
if not os.path.exists(individual_reports_path):
    os.makedirs(individual_reports_path)

# find table element
table = soup.find('table', {'class': 'table mb-3'})

missing_reports = []

rows = table.find_all('tr')
num_rows = len(rows)
print(f"Number of rows: {num_rows}")

# loop through rows in table
for row in table.find_all('tr')[1:]:
    # extract data from columns
    date_provided = row.find('span', {'data-bind': 'text: date_provided_pretty'}).text

    # Convert date_provided to datetime object
    try:
        dt = datetime.datetime.strptime(date_provided, '%b %d, %Y')
    except ValueError:
        dt = datetime.datetime.strptime(date_provided + ' ' + str(datetime.datetime.now().year), '%b %d %Y')

    # Format the datetime object into the desired string format
    formatted_date_provided = dt.strftime('%Y%m%d')

    partner_name = row.find('h6', {'data-bind': 'text: partner_name'}).text
    partner_name = re.sub(r'[^a-zA-Z0-9\s]', '', partner_name)
    partner_name = partner_name.replace(" ", "")

    csv_download_url = row.find('a', {'data-bind': 'attr: {href: csv_download_url()}'}).get('href')

    parsed_url = urlparse(csv_download_url)
    query_params = parse_qs(parsed_url.query)
    report_id = query_params.get('report_id', [None])[0]
    
    # download CSV file
    response = requests.get(csv_download_url, cookies=cookie)

    # Check if the response contains the "Could not locate resource" message
    if '{"message":"Could not locate resource.","resource":null}' in response.text:
        print(f'Report {report_id} not found.')
        missing_reports.append([formatted_date_provided, partner_name, report_id, csv_download_url])
    else:
        filename = f"{partner_name}_{formatted_date_provided}_report{report_id}.csv"
        with open(f"{individual_reports_path}/{filename}", 'wb') as f:
            print(f'Report {report_id} downloaded')
            f.write(response.content)
    continue

# Write the missing reports to a CSV file
if missing_reports:
    with open(f"{date_path}/_{date_downloaded}_missing_reports.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Formatted Date Provided', 'Partner Name', 'Report ID', 'CSV Download URL'])
        for report in missing_reports:
            writer.writerow(report)
    print(f'{len(missing_reports)} missing reports written to missing_reports.csv')
else:
    print('No missing reports found')
