import requests
import json
import time
import re
from datetime import datetime

# URLs - Using v2 for the app list
APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"

# Configuration
START_YEAR = 2015
END_YEAR = 2020
OUTPUT_FILE = "steam_games_2015_2020.json"

# Steam is very strict. 1.5s is safe. 
# 1.0s is faster but carries a higher risk of a temporary IP block.
REQUEST_DELAY = 1.2  

def fetch_all_app_ids():
    """Fetches the global list of all AppIDs from Steam."""
    print("Fetching global AppID list from Steam...")
    try:
        r = requests.get(APP_LIST_URL, timeout=30)
        r.raise_for_status()
        apps = r.json()["applist"]["apps"]
        print(f"Successfully retrieved {len(apps)} total AppIDs.")
        return apps
    except Exception as e:
        print(f"Error fetching AppID list: {e}")
        return []

def fetch_release_year(app_id):
    """Queries appdetails for a specific ID and extracts the year."""
    params = {"appids": app_id, "l": "english"}
    try:
        r = requests.get(APP_DETAILS_URL, params=params, timeout=10)
        
        # Handle Rate Limiting (HTTP 429)
        if r.status_code == 429:
            print(f"\n[!] Rate limited at AppID {app_id}. Cooling down for 30 seconds...")
            time.sleep(30)
            return None

        r.raise_for_status()
        payload = r.json().get(str(app_id))
        
        if not payload or not payload.get("success"):
            return None

        data = payload["data"]
        
        # STAGE 1 FILTER: Must be a game
        if data.get("type") != "game":
            return None

        release = data.get("release_date", {})
        date_str = release.get("date")
        
        # Ignore if no date or if it's not out yet
        if not date_str or release.get("coming_soon"):
            return None

        # STAGE 1 FILTER: Extract year using Regex (handles "2015", "Dec 2015", "15 Oct, 2015")
        year_match = re.search(r'(\d{4})', date_str)
        if year_match:
            year = int(year_match.group(1))
            return year, data.get("name")
            
    except Exception:
        return None
    return None

def main():
    all_apps = fetch_all_app_ids()
    if not all_apps:
        print("Could not retrieve apps. Exiting.")
        return

    # --- SET YOUR LIMIT HERE ---
    # [1000:3000] means skip the first 1000, then take the next 2000 apps.
    target_slice = all_apps[1000:3000]
    total_to_process = len(target_slice)
    
    print(f"Starting scan of {total_to_process} apps (Indices 1000 to 3000)...")
    
    results = []

    for i, app in enumerate(target_slice, start=1000):
        app_id = app["appid"]
        
        info = fetch_release_year(app_id)
        
        if info:
            year, name = info
            if START_YEAR <= year <= END_YEAR:
                results.append({
                    "app_id": app_id,
                    "name": name,
                    "release_year": year
                })
                print(f"FOUND: [{year}] {name}")

        # Progress update every 10 apps
        if i % 10 == 0:
            print(f"Processed {i}/3000...", end="\r")

        # Periodic save to disk so you don't lose data if it crashes
        if i % 50 == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

        time.sleep(REQUEST_DELAY)

    # Final Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n\nDone! Saved {len(results)} valid games to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()