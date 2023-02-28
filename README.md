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

6. If this returns an error, you may need to restart your computer before trying again. Installation may take a few minutes.

## Usage

1. After packages have installed, type ```python avalanche.py``` and press Enter to run the script.

2. Follow the on-screen instructions to download reports or generate aggregate reports.

3. You will need to run the script once to download your reports, then a second time to aggregate the reports into combined files.

### Download Reports

- After selecting "Download all reports," a login page for the Materia Dashboard will appear. 

- Enter your login credentials and click the submit button. 

- If you have multiple artists under your account, you will be asked to select an artist. 

- The script will proceed to automatically download all available reports.

- A reports summary will be available once all reports have finished downloading.

### Aggregate Reports

- This script will prompt you to choose which folder of reports you would like to aggregate. It will then combine all of the individual reports into a simple aggregate report, which sums the totals for each unique product found in your report. The script will also generate a detailed aggregate report which simply combines all of your reports into a single CSV file. 

- This script might give you an arguments error at first, but it should still work if you let it finish.

- It is worth noting that the "Units" column of the aggregated report is combining sales and streams of single tracks. I will try to differentiate the two in the future, but for now it's still useful as a popularity metric.

> Warning! The detailed aggregate report file will be very large! Please open with caution.

## Missing Reports

Missing reports are reports that appear in the list of reports on an artist's dashboard but are unable to be downloaded. This seems to be an issue on Materia's end. Attempting to download the report just opens a page with the following message:

```{"message":"Could not locate resource.","resource":null}```

If the script encounters any missing reports, it will make note of the missing report in the report summary. If the report summary says you have missing reports, please manually verify this before contacting Materia Support to resolve the issue.

Missing reports still have an "amount" displayed on the reports page which you can see in the report summary. 
