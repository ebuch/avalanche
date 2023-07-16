# This file is licensed under the MIT License.
# See LICENSE for more information.

import os
import re
import csv
import sys
import time
import logging
import datetime
import requests
from colorama import init
from termcolor import colored
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

init()

# Start a browser session
driver = webdriver.Chrome()
driver.get("https://auth.dash.materiamusic.com/u/login/")

print(colored("Log into the Materia Dashboard to continue.", "cyan"))

wait = WebDriverWait(driver, 60)
wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Welcome home'))

page_source = driver.page_source

# Check if the user is logged in
logged_in = "Welcome home" in driver.page_source

if not logged_in:
    print(colored("Login failed.", "red"))
else:
    print(colored("Login successful!", "green"))

    # create BeautifulSoup object
    soup = BeautifulSoup(page_source, 'html.parser')

    artists = soup.select('div.card.team__item a[href*="/artist/"][data-bind*="url_admin()"] + div h4.card-title a[href*="/artist/"][data-bind*="name()"]')

    # Check if there are multiple artists
    if len(artists) > 1:
        print("Multiple artists found. Please select one:")
        for i, artist in enumerate(artists):
            print(f"{i+1}. {artist.get_text()}")
                    
        selected_artist_index = int(input("Enter the artist number: ")) - 1
        selected_artist = artists[selected_artist_index]
    else:
        selected_artist = artists[0]

    # Extract text and artist ID
    artist_name = selected_artist.get_text()
    artist_id = selected_artist["href"].split("/")[-1]
    print(colored(f"Downloading reports for {artist_name}. This might take several minutes... go make some tea!", "yellow"))

    # navigate to the reports page
    artist_url = f"https://dash.materiamusic.com/artist/{artist_id}/reports"
    driver.get(artist_url)

    # wait 10 seconds for the table to load
    print(colored("Allowing 10 seconds for the reports table to load completely.", "magenta"))
    time.sleep(10)

    # update beautifulsoup source
    reports_page_source = driver.page_source
    soup = BeautifulSoup(reports_page_source, 'html.parser')

    # find table and count rows
    table = soup.find("table", {"class": "table mb-3"})
    rows = table.find_all("tr")
    print(colored(f"Number of reports found: {len(rows) - 1}", "yellow"))

    # Set the download date
    date_downloaded = datetime.datetime.now().strftime("%Y-%m-%d")

    # define paths to directories
    base_path = f"Reports/{artist_name}"
    date_path = os.path.join(base_path, date_downloaded)
    individual_reports_path = os.path.join(date_path, "Individual Reports")

    # create directories if they don't exist
    os.makedirs(individual_reports_path, exist_ok=True)

    # define path to reports summary file
    reports_summary_file = os.path.join(date_path, f"{date_downloaded}_reports_summary.csv")

    # check if reports summary file exists and create it with header row if it doesn't
    if not os.path.isfile(reports_summary_file):
        with open(reports_summary_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date Provided", "Partner Name", "Report ID", "Tracking URL", "Amount from Reports Page", "Amount from Details View", "Report Found"])

    # extract the cookies as a dictionary
    cookies = driver.get_cookies()
    auth_cookie = next(cookie for cookie in cookies if cookie['name'] == 'materiacollective')['value']

    # set the cookie as a dictionary
    cookie = {
        'materiacollective': auth_cookie
    }

    # initialize total variables
    total_amount_from_reports_page = 0
    successful_downloads = 0

    # loop through rows in table
    num_reports = 0
    total_stats_total_amount = 0
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
            print(colored(f'({num_reports + 1}/{len(rows) - 1}) Report {report_id} not found.', "red"))
            report_found = False

        if report_found:
            partner_name = partner_name.replace(' ', '')
            filename = f"{partner_name}_{formatted_date_provided}_Report{report_id}.csv"
            with open(f"{individual_reports_path}/{filename}", 'wb') as f:
                print(colored(f'({num_reports + 1}/{len(rows) - 1}) Report {report_id} successfully downloaded.', "green"))
                f.write(response.content)

        # add row to reports summary file
        reports_summary_row = [formatted_date_provided, partner_name, report_id, amount, report_found]
        with open(reports_summary_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(reports_summary_row)

            # add to totals
            total_amount_from_reports_page += float(amount[1:].replace(',', ''))
            if report_found:
                successful_downloads += 1

        num_reports += 1   
        continue
    
    # Append totals row to reports summary file
    with open(reports_summary_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['', 'Totals', '', '', total_amount_from_reports_page, f'{successful_downloads} / {len(rows) - 1}'])

    formatted_total_amount = f'${float(total_stats_total_amount):,.2f}'
    print(colored(f"Downloading complete! A download summary has been generated. To generate aggregated reports, re-run avalanche.py.", "cyan"))
