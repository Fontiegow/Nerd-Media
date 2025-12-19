import os
from pathlib import Path
from dotenv import load_dotenv

# Project Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_RAW = BASE_DIR / "data/raw"

# Path to .env file
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Make sure the raw data directory exists
DATA_RAW.mkdir(parents=True, exist_ok=True)

# API Configuration
# STEAM_APP_LIST_URL = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
STEAM_APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2"

# Recommended to use an API key for higher rate limits
STEAM_API_KEY = os.getenv("STEAM_API_KEY") 
USER_AGENT = "SteamDataCollector/0.1 (research)"