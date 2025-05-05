import time
import random
import string
import requests

# CONFIGURATION
WEBHOOK_URL = "http://localhost:8080/webhook"
WEBHOOK_SECRET = "supersecret"  # must match your FastAPI WEBHOOK_SECRET
SYMBOLS = ["AAPL", "GOOG", "TSLA", "MSFT", "AMZN"]

def random_payload():
    ticker = random.choice(SYMBOLS)
    action = random.choice(["buy", "sell"])
    quantity = random.randint(1, 10)
    base_price = random.uniform(100, 500)
    price = round(base_price * random.uniform(0.9, 1.1), 2)
    return {
        "ticker": ticker,
        "action": action,
        "quantity": quantity,
        "price": price,
    }

def main():
    print(f"Starting load generator, posting to {WEBHOOK_URL} every 2s\n")
    while True:
        payload = random_payload()
        try:
            resp = requests.post(
                WEBHOOK_URL,
                json=payload,
                headers={"x-webhook-secret": WEBHOOK_SECRET},
                timeout=5
            )
            print(
                f"[{time.strftime('%H:%M:%S')}] → {payload}  "
                f"→ status {resp.status_code}  {resp.text!r}"
            )
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ERROR posting: {e}")
        time.sleep(2)

if __name__ == "__main__":
    main()
