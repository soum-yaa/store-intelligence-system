import time
import requests
import os

API_URL = "http://127.0.0.1:8000/stores/STORE_001/metrics"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    while True:
        clear_screen()

        try:
            response = requests.get(API_URL)
            data = response.json()

            print("STORE INTELLIGENCE LIVE DASHBOARD")
            print("=" * 40)
            print(f"Store ID: {data['store_id']}")
            print(f"Total Events: {data['total_events']}")
            print(f"Unique Visitors: {data['unique_visitors']}")
            print(f"Entries: {data['entries']}")
            print(f"Exits: {data['exits']}")
            print(f"Conversion Rate: {data['conversion_rate']}%")
            print(f"Queue Depth: {data['queue_depth']}")
            print(f"Abandonment Rate: {data['abandonment_rate']}%")
            print("=" * 40)
            print("Refreshing every 5 seconds...")

        except Exception as e:
            print("Dashboard error:", e)

        time.sleep(5)


if __name__ == "__main__":
    main()