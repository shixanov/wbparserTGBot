import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME")
GROUP_ID = int(os.getenv("GROUP_ID", 0))

VERSION = '1.0'