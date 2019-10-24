import glob
import csv

from parser import Parser

CSV_HEADER = ["date", "famille_transport", "ligne", "regularite"]
dates = set()
data = []

for file in glob.glob("data/*.html"):
    print(f"Processing {file}")
    with open(file) as f:
        html_content = f.read()
    parsed = Parser(html_content)
    if parsed.date() in dates:
        raise ValueError("Duplicate date")
    dates.add(parsed.date())
    data.extend(parsed.to_list())

with open("regularite.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(CSV_HEADER)
    writer.writerows(data)
