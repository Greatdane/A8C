#Quick and dirty GitHub API call for PA Triagers to get issue date from wp-calypso
import requests
import csv
from datetime import datetime

token = "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"
headers = {'Authorization': f'token {token}'}

filename = 'file.csv'

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    with open('output.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for row in datareader:
            try:
                print("Trying URL: " + str(row)[2:-2])
                row_list = []
                row_list.append(str(row)[2:-2])
                api_url = "https://api.github.com/repos/" + str(row)[21:]
                response = requests.get(api_url, headers=headers)
                data = response.json()
                # Get state (open or closed)
                row_list.append(data["state"])

                # Get days between open and closed (if closed)
                if data["state"] == "closed":
                    created_at = datetime.strptime(data["created_at"][:10], '%Y-%m-%d')
                    closed_at = datetime.strptime(data["closed_at"][:10], '%Y-%m-%d')
                    row_list.append((closed_at-created_at).days)
                else:
                    row_list.append("")

                # Get labels (Bug, Feature Request or Enhancement)
                for label in data["labels"]:
                    if label['name'] == "[Type] Bug":
                        row_list.append("[Type] Bug")
                    if label['name'] == "[Type] Feature Request":
                        row_list.append("[Type] Feature Request")
                    if label['name'] == "[Type] Enhancement":
                        row_list.append("[Type] Enhancement")

                writer.writerow(row_list)
                print("Wrote data; " + str(row_list))
            except Exception as e:
                print("Failed: " + str(e))
