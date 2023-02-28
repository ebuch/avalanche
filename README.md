# avalanche

## For the planet!

avalanche is a set of Python scripts for Materia artists that enables them to conveniently download and aggregate reports from the Materia Dashboard. These scripts are not created, maintained, or endorsed by Materia Music. Do not contact Materia Support with issues pertaining to these scripts.

## Installation

1. Install Python. You can download the latest version of Python from the [official website](https://www.python.org/downloads/). Be sure to select the "Add Python to PATH" option during the installation process.

2. Install Google Chrome.

3. Download or clone this repository onto your local machine.

4. Using a terminal or command prompt window, navigate to the root directory of the avalanche project by typing "cd C:\path\to\avalanche" (replace "C:\path\to\avalanche" with the actual path to your avalanche project).

5. Install the required Python packages by running the following command:

```pip install -r requirements.txt```

## Usage

1. After packages have installed, type ```python avalanche.py``` and press Enter to run the script.

2. Follow the on-screen instructions to download reports or generate aggregate reports.

3. You will need to run the script once to download your reports, then a second time to aggregate the reports into combined files.

### Download Reports

- You will be prompted to provide your Materia Dashboard login username and password, as well as the artist ID associated with an artist managed under your account. To find your artist ID, log into the Materia Dashboard and click on the artist you wish to generate reports for. The number at the end of the URL is the artist ID. Your login credentials are not stored by the script.

- Upon running the download reports script, a browser window will automatically pop open and log you into the dashboard. It will then automatically go through and download all of your reports and scrape data from the website to build a Reports Summary file. This may take several minutes so go make yourself a cup of tea.

### Aggregate Reports

- This script will prompt you to choose which folder of reports you would like to aggregate. It will then combine all of the individual reports into a simple aggregate report, which sums the totals for each unique product found in your report. The script will also generate a detailed aggregate report which simply combines all of your reports into a single CSV file. 

- It is worth noting that the "Units" column of the aggregated report is combining sales and streams of single tracks. I will try to differentiate the two in the future, but for now it's still useful as a popularity metric.

> Warning! The detailed aggregate reports file will be very large! Please open with caution.

## Missing Reports

Missing reports are reports that appear in the list of reports on an artist's dashboard but are unable to be downloaded. This seems to be an issue on Materia's end. Attempting to download the report just opens a page with the following message:

```{"message":"Could not locate resource.","resource":null}```

If the script encounters any missing reports, it will make note of the missing report in the Reports Summary. If this report summary says you have missing reports, please manually verify this before contacting Materia Support to resolve the issue.
