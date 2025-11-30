import requests
import time
import json
import csv
import argparse
from datetime import datetime

# 🔗 Webhook для Discord
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1444642798417477703/VBYncVbkwFO6qsfc4PGb4cxi2BuPK-BKyrBie5jGw9GbTn65TuR3Z9ZZY0wxLcZHIOj7"  

# 📨 Відправлення повідомлення у Discord
def send_discord_alert(message):
    payload = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")

# 🔎 Перевірка одного API endpoint
def check_endpoint(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = round(time.time() - start, 3)
        return {
            "endpoint": url,
            "status_code": response.status_code,
            "response_time": elapsed,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except requests.exceptions.RequestException as e:
        return {
            "endpoint": url,
            "status_code": "ERROR",
            "response_time": None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": str(e)
        }

# 💾 Збереження у JSON
def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 💾 Збереження у CSV
def save_to_csv(data, filename):
    fieldnames = ["timestamp", "endpoint", "status_code", "response_time", "error"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

# 🚀 Основна функція
def main():
    parser = argparse.ArgumentParser(description="API Monitoring Script")
    parser.add_argument("--endpoints", type=str, default="https://api.github.com",
                        help="Comma-separated list of API endpoints")
    parser.add_argument("--format", type=str, choices=["json", "csv"], default="json",
                        help="Output format (json or csv)")
    parser.add_argument("--file", type=str, help="Output filename")

    args = parser.parse_args()

    endpoints = [e.strip() for e in args.endpoints.split(",")]
    results = [check_endpoint(url) for url in endpoints]

    for result in results:
        status = result["status_code"]
        if not (isinstance(status, int) and 200 <= status < 300):
            message = f"⚠️ API ALERT: {result['endpoint']} failed! Status: {result['status_code']}, Response time: {result['response_time']}"
            send_discord_alert(message)

    filename = args.file or f"results.{args.format}"

    if args.format == "json":
        save_to_json(results, filename)
    else:
        save_to_csv(results, filename)

    print(f"✅ Results saved to {filename}")

if __name__ == "__main__":
    main()
