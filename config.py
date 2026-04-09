import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_TELEGRAM_ID = int(os.getenv('OWNER_TELEGRAM_ID')) 

USE_WEBHOOKS = os.getenv('USE_WEBHOOKS', 'false').lower() == 'true'
WEBHOOK_URL = os.getenv('WEBHOOK_URL') or os.getenv('RENDER_EXTERNAL_URL')

# Order ID Counters (in production, use database)
ORDER_COUNTERS = {
    'handkerchief': 1,
    'clothes': 1
}