import requests, csv, os

CHANNEL_ID = "3012807"
N = 91
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results={N}"

FILE = "wemos_log.csv"

HEADERS = [
    "time",
    "cahaya",
    "soil",
    "temperature",
    "humidity",
    "fuzzy_output",
    "pump_status",
    "pump_duration"
]

existing_times = set()

if os.path.isfile(FILE):
    with open(FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("time"):
                existing_times.add(row["time"])

response = requests.get(URL)
feeds = response.json().get("feeds", [])

new_rows = []

for data in feeds:
    created_at = data.get("created_at")
    if not created_at or created_at in existing_times:
        continue

    new_rows.append([
        created_at,
        data.get("field1"),
        data.get("field2"),
        data.get("field3"),
        data.get("field4"),
        data.get("field5"),
        data.get("field6"),
        data.get("field7")
    ])

if new_rows:
    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(HEADERS)

        writer.writerows(new_rows)
    
    print(f"Appended {len(new_rows)} new rows to {FILE}.")
else:
    print("No new data to append.")
