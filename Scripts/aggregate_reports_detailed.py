# This file is licensed under the MIT License.
# See LICENSE for more information.

import os
import sys
import pandas as pd
import argparse
from colorama import init
from termcolor import colored

init()

# create argument parser
parser = argparse.ArgumentParser(description='Aggregate reports for a given artist and date downloaded')

# add arguments
parser.add_argument('artist_folder', help='Name of the artist to aggregate reports for')
parser.add_argument('date_folder', help='Name of the date downloaded folder to aggregate reports for')

# parse arguments
args = parser.parse_args()

# access the arguments
if hasattr(args, 'artist_folder') and hasattr(args, 'date_folder'):
    artist_folder = args.artist_folder.strip('"')
    date_folder = args.date_folder.strip('"')
else:
    print('Error: Missing required arguments')
    sys.exit(1)

# Get the path to the root folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(ROOT_DIR, "..", "Reports")

# set the paths for the individual reports and the aggregate report
individual_reports_path = os.path.join(ROOT_DIR, "Reports", artist_folder, date_folder, "Individual Reports")
aggregate_report_path = os.path.join(ROOT_DIR, "Reports", artist_folder, date_folder, f"{date_folder}_detailed_aggregate_report.csv")

# loop through the individual reports folder and combine the CSV files into a single data frame
aggregate_df = pd.DataFrame()
for filename in os.listdir(individual_reports_path):
    if filename.endswith(".csv"):
        df = pd.read_csv(os.path.join(individual_reports_path, filename), skiprows=2)
        aggregate_df = pd.concat([aggregate_df, df], ignore_index=True)

# save the aggregated data frame to a CSV file
aggregate_df.to_csv(aggregate_report_path, index=False)

print(colored(f"Detailed aggregated report for {date_folder} has been created at {aggregate_report_path}.", "green"))
