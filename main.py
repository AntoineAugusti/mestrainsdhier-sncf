import glob
import csv
import logging

from parser import Parser

CSV_HEADER = ["date", "famille_transport", "ligne", "regularite", "explication"]
INCIDENTS_HEADER = ["date", "famille_transport", "ligne", "incidents"]
dates = set()
data = []
incidents = []

for filename in sorted(glob.glob("data/*.html")):
    print(f"Processing {filename}")
    with open(filename) as f:
        html_content = f.read()
    parsed = Parser(html_content)
    if parsed.date() in dates:
        logging.exception(f"Duplicate date: {parsed.date()}")
    dates.add(parsed.date())
    try:
        data.extend(parsed.to_list())
        incidents.extend(parsed.incidents())
    except Exception as e:
        logging.exception(e.message)

with open("data/regularite.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(CSV_HEADER)
    writer.writerows(data)

with open("data/incidents.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(INCIDENTS_HEADER)
    writer.writerows(incidents)
