import os
from dotenv import load_dotenv

load_dotenv()

STEAM_ID = os.environ.get("STEAM_ID")
STEAM_ID_HEX = os.environ.get("STEAM_ID_HEX")
STRIVE_ID = os.environ.get("STRIVE_ID")
STEAM_USERNAME = os.environ.get("STEAM_USERNAME")
STEAM_PASSWORD = os.environ.get("STEAM_PASSWORD")
