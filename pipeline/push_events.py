import json
import requests

API_URL = "http://127.0.0.1:8000/events/ingest"

EVENTS_FILE = "output/events.jsonl"


def main():

    events = []

    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            events.append(json.loads(line))

    print(f"Loaded {len(events)} events")

    response = requests.post(
        API_URL,
        json=events
    )

    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()