import os
import re
import csv
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

# Set the artist ID
artist_id = 657

# Set the authentication cookie
cookie = {
    'materiacollective': '8dom4kdrgvifdcj0gk2hffgrpsqb0gft'
}

# Set the download date
date_downloaded = datetime.datetime.now().strftime("%Y%m%d")

# Start a browser session
driver = webdriver.Chrome()

# Navigate to the login page
driver.get(f"https://dash.materiamusic.com/artist/{artist_id}/reports")

wait = WebDriverWait(driver, 5)

# Find the username and password fields and enter your login information
username_field = driver.find_element(By.ID, "username")
username_field.send_keys('buchholzeric@gmail.com')
username_field.send_keys(Keys.RETURN)

password_field = driver.find_element(By.ID, "password")
password_field.send_keys('x8fMo?xm99yX3EP6')
password_field.send_keys(Keys.RETURN)

# Wait for the table to load
time.sleep(5)

# get page source using Selenium
page_source = driver.page_source

# create BeautifulSoup object
soup = BeautifulSoup(page_source, 'html.parser')

# find artist name
artist_name = soup.find('div', {'class': 'entity-name'}).text.strip()
print(artist_name)

# Create a directory to save the downloaded reports
if not os.path.exists(f"{os.getcwd()}/Reports"):
    os.mkdir(f"{os.getcwd()}/Reports")

path_to_reports = f"{os.getcwd()}/Reports/{date_downloaded}"

if not os.path.exists(path_to_reports):
    os.mkdir(path_to_reports)

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
        with open(f"{path_to_reports}/{filename}", 'wb') as f:
            print(f'Report {report_id} downloaded')
            f.write(response.content)
    continue

# Write the missing reports to a CSV file
if missing_reports:
    with open(f"{path_to_reports}/_{date_downloaded}_missing_reports.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Formatted Date Provided', 'Partner Name', 'Report ID', 'CSV Download URL'])
        for report in missing_reports:
            writer.writerow(report)
    print(f'{len(missing_reports)} missing reports written to missing_reports.csv')
else:
    print('No missing reports found')
