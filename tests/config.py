import os
from dotenv import load_dotenv

load_dotenv()

steam_id = os.environ.get("STEAM_ID")
steam_id_hex = os.environ.get("STEAM_ID_HEX")
strive_id = os.environ.get("STRIVE_ID")
