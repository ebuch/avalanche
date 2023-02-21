import requests
import os

start_report_id = 46  # starting report id
end_report_id = 52  # ending report id
artist_id = 657  # artist id

# Set the authentication cookie
cookie = {
    'materiacollective': '591jd25e98ujl4h12b8nme8s3pfk23l6'
}

# Loop through the report URLs, from 1 to 4000

for report_id in range(start_report_id, end_report_id):
    # Construct the report URL
    report_url = f'https://dash.materiamusic.com/api/1/artist/aggregate_report_csv/?artist_id={artist_id}&report_id={report_id}'

    # Send a GET request to the report URL with the authentication cookie in the headers
    response = requests.get(report_url, cookies=cookie)

    # Check if the response contains the "Could not locate resource" message
    if '{"message":"Could not locate resource.","resource":null}' in response.text:
        print(f'Report {report_id} not found')
    else:
        # Construct the filename for the CSV file
        filename = f'{report_id}.csv'
        # Save the response content to a file in the reports folder
        with open(os.path.join('reports', filename), 'wb') as f:
            f.write(response.content)
        print(f'Report {report_id} downloaded')
