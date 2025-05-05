import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ALPACA_API_KEY: str = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY: str = os.getenv("ALPACA_SECRET_KEY")
    ALPACA_BASE_URL: str = "https://paper-api.alpaca.markets"
    ALPACA_DATA_URL: str = "https://data.alpaca.markets"
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "supersecret")
    RETRY_LIMIT: int = 2
    RETRY_BACKOFF_SECONDS: int = 2

settings = Settings()
