import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

CLIENT_ID = str(os.getenv("CLIENT_ID"))
CLIENT_SECRET = str(os.getenv("CLIENT_SECRET"))

admins_id = [
    782389029, # Влад
    473151013,  # Славик
]
