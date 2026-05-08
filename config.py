import os
from dotenv import load_dotenv

load_dotenv()

LEETCODE_USERNAME = os.getenv("LEETCODE_USERNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MONGO_URI = os.getenv("MONGO_URI")