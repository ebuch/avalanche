# Avalanche

A set of Python scripts for Materia Artists that enables them to conveniently download and aggregate reports from the Materia Dashboard. These scripts are not created, maintained, or endorsed by Materia Music. Do not contact Materia Support with issues pertaining to these scripts.

## Installation

1. Install Python. You can download the latest version of Python from the [official website](https://www.python.org/downloads/).

2. Install Google Chrome.

3. Download or clone this repository onto your local machine.

4. Navigate to the directory containing the scripts by opening a terminal or command prompt window and using the `cd` command.

5. Install the required Python packages by running the following command:

```pip install -r requirements.txt```

## Usage

1. Open the `download_reports.py` file in a text editor.

2. Modify the following variables in the `Setup` section of the script:

- `artist_name`: Set this to the name of the artist whose reports you want to download.
- `artist_id`: Set this to the ID of the artist whose reports you want to download. When viewing your artist page on the Materia Dashboard, the number at the end of the URL is your artist ID.
- `login_email`: Set this to the email address you use to log in to your Materia Dashboard account.
- `login_password`: Set this to the password you use to log in to your Materia Dashboard account.

3. Save the modified script.

4. Open a terminal or command prompt window and navigate to the directory containing the `download_reports.py` script.

5. Run the script by entering the following command:

```python download_reports.py```

The script will log in to your Materia Dashboard account, download all available reports for the specified artist, and save them to a folder in the `avalanche` directory.

Note: If the script encounters any missing reports, it will create a CSV file in the same folder with information about the missing reports.

## Missing Reports

Missing reports are reports that appear in the list of reports on an artist's dashboard but are unable to be downloaded. This seems to be an issue on Materia's end with how permissions are handled. Attempting to download the report just opens a page with the following message:

```{"message":"Could not locate resource.","resource":null}```

If the script encounters any missing reports, it will create a CSV file in the same folder with information about the missing reports. If this script says you have missing reports, please manually verify this before contacting Materia Support to resolve the issue.
