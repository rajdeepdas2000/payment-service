# Use local URL for local testing
# Use Render URL for deployed testing

import requests
import json

URL = "http://127.0.0.1:8000/events" #local URL
# URL = "https://payment-service-u2p7.onrender.com/events" #Render URL

with open("sample_events.json") as f:
    events = json.load(f)

success = 0
fail = 0

for i, e in enumerate(events):
    try:
        res = requests.post(URL, json=e, timeout=5)
        if res.status_code == 200:
            success += 1
        else:
            fail += 1
    except Exception:
        fail += 1

    if i % 200 == 0:
        print(f"{i} processed | success={success} fail={fail}")

print(f"FINAL: success={success}, fail={fail}")