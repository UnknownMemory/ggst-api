import os
from dotenv import load_dotenv

load_dotenv()

steamID = os.environ.get("STEAM_ID")
steamIDHex = os.environ.get("STEAM_ID_HEX")
striveID = os.environ.get("STRIVE_ID")