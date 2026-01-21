import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_TELEGRAM_ID = os.getenv('OWNER_TELEGRAM_ID')  # Your Telegram ID

# Order ID Counters (in production, use database)
ORDER_COUNTERS = {
    'handkerchief': 1,
    'clothes': 1
}