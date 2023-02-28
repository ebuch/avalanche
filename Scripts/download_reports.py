import os
import re
import csv
import sys
import time
import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Prompt the user for their authentication credentials and artist ID
login_email = input("Enter your Materia Dashboard login email: ")
login_password = input("Enter your Materia Dashboard login password: ")
artist_id = input("Enter your Materia Dashboard artist ID: ")

# Set the download date
date_downloaded = datetime.datetime.now().strftime("%Y-%m-%d")

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

# get artist name from dashboard
artist_name = soup.find('div', {'class': 'entity-name'}).text

# define paths to directories
base_path = f"Reports/{artist_name}"
date_path = os.path.join(base_path, date_downloaded)
individual_reports_path = os.path.join(date_path, "Individual Reports")

# create directories if they don't exist
os.makedirs(individual_reports_path, exist_ok=True)

# find table and count rows
table = soup.find("table", {"class": "table mb-3"})
rows = table.find_all("tr")
print(f"Number of rows in table: {len(rows) - 1}")

# define path to reports summary file
reports_summary_file = os.path.join(date_path, f"{date_downloaded}_reports_summary.csv")

# check if reports summary file exists and create it with header row if it doesn't
if not os.path.isfile(reports_summary_file):
    with open(reports_summary_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date Provided", "Partner Name", "Report ID", "Tracking URL", "Amount from Reports Page", "Amount from Details View", "Report Found"])

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
    formatted_date_provided = dt.strftime('%Y-%m-%d')

    partner_name = row.find('h6', {'data-bind': 'text: partner_name'}).text
    partner_name = re.sub(r'[^a-zA-Z0-9\s]', '', partner_name)
    partner_name = partner_name.replace(" ", "")

    amount = row.find('span', {'data-bind': 'accounting_display_number: amount_fixed'}).text

    csv_download_url = row.find('a', {'data-bind': 'attr: {href: csv_download_url()}'}).get('href')

    parsed_url = urlparse(csv_download_url)
    query_params = parse_qs(parsed_url.query)
    report_id = query_params.get('report_id', [None])[0]

    report_found = True
    
    # download CSV file
    response = requests.get(csv_download_url, cookies=cookie)

    # Check if the response contains the "Could not locate resource" message
    if '{"message":"Could not locate resource.","resource":null}' in response.text:
        print(f'Report {report_id} not found.')
        report_found = False

    if report_found:
        filename = f"{partner_name}_{formatted_date_provided}_report{report_id}.csv"
        with open(f"{individual_reports_path}/{filename}", 'wb') as f:
            print(f'Report {report_id} downloaded')
            f.write(response.content)

    # Navigate to tracking URL and get stats_total_amount if report is missing
    tracking_url = row.find('a', {'data-bind': 'attr: {href: tracking_url()}'}).get('href')
    driver.get(tracking_url)
    # Wait up to 10 seconds for the stats_total_amount element to be present on the page
    wait = WebDriverWait(driver, 10)
    stats_total_amount = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'stats_total_amount')))

    try:
        stats_total_amount = driver.find_element(By.CLASS_NAME, 'stats_total_amount').text.replace(',', '')
        print(f"Found stats_total_amount {stats_total_amount} for report {report_id}")
    except:
        stats_total_amount = ""
        print(f"Unable to get stats_total_amount for report {report_id}")

    # add row to reports summary file
    reports_summary_row = [formatted_date_provided, partner_name, report_id, tracking_url, amount, stats_total_amount, report_found]
    with open(reports_summary_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(reports_summary_row)

    continue
