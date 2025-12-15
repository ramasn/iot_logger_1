import requests, csv, os

CHANNEL_ID = "3012807"
N = 91
url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results={N}"

response = requests.get(url)
feeds = response.json()["feeds"]

file = "wemos_log.csv"
exists = os.path.isfile(file)

with open(file, "a", newline="") as f:
    writer = csv.writer(f)

    if not exists:
        writer.writerow([
            "time",
            "cahaya",
            "soil",
            "temperature",
            "humidity",
            "fuzzy_output",
            "pump_status",
            "pump_duration"
        ])

    for data in feeds:
        writer.writerow([
            data.get("created_at"),
            data.get("field1"),
            data.get("field2"),
            data.get("field3"),
            data.get("field4"),
            data.get("field5"),
            data.get("field6"),
            data.get("field7")
        ])