import requests
import json

URL = "http://127.0.0.1:8000/events"

with open("sample_events.json") as f:
    events = json.load(f)

for e in events:
    requests.post(URL, json=e)