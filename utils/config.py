import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))
STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
STANDARD_PASSWORD = os.getenv("STANDARD_PASSWORD", "secret_sauce")
