import requests
import pandas as pd
import sys
import os
from datetime import datetime
from pathlib import Path

# Import from local files
try:
    from config import STEAM_APP_LIST_URL, STEAM_API_KEY, DATA_RAW
    # from utils import polite_sleep # Reserved for future loops
except ImportError:
    print("❌ Error: Could not import config. Make sure config.py is in the same directory.")
    sys.exit(1)

# Fix Unicode display issues in Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def fetch_steam_app_list():
    """
    Fetches the master list of all Steam apps.
    Uses ISteamApps/GetAppList/v2 interface.
    """
    print(f"[{datetime.now()}] 🌐 Connecting to Steam API...")
    
    # Clean the URL to ensure no trailing slashes interfere with parameters
    clean_url = STEAM_APP_LIST_URL.rstrip('/')
    
    params = {
        'key': STEAM_API_KEY,
        'format': 'json'
    }
    
    try:
        # Steam's v2 API can be large (>10MB), so we set a generous timeout
        response = requests.get(clean_url, params=params, timeout=60)
        
        # Check for specific HTTP errors
        if response.status_code == 404:
            print(f"❌ Error 404: API endpoint not found. Please check the URL in config.py.")
            print(f"Attempted URL: {clean_url}")
            return None
        elif response.status_code == 403:
            print("❌ Error 403: Forbidden. Your API Key is likely invalid or has been restricted.")
            return None
            
        response.raise_for_status()
        data = response.json()
        
        # Structure for ISteamApps/GetAppList/v2 is: {"applist": {"apps": [...]}}
        apps = data.get('applist', {}).get('apps', [])
        
        if not apps:
            print("⚠️ Response received but the app list is empty.")
            return None
            
        print(f"✅ Successfully fetched {len(apps)} raw entries.")
        return apps

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return None
    except ValueError:
        print("❌ JSON Decode Error: The server did not return valid JSON.")
        return None

def process_and_save_raw(apps):
    """
    Cleans the raw list and saves it as a Parquet file.
    """
    if not apps:
        print("⚠️ No data to process.")
        return

    print(f"[{datetime.now()}] ⚙️ Processing and cleaning data...")
    
    # 1. Convert to DataFrame
    df = pd.DataFrame(apps)
    
    # 2. Basic Cleaning
    initial_count = len(df)
    
    # Remove rows where name is null or just whitespace
    if 'name' in df.columns:
        df = df[df['name'].fillna('').str.strip() != ""]
    
    # 3. Remove duplicates based on appid
    df = df.drop_duplicates(subset=['appid'])
    
    # 4. Add Metadata
    df['source'] = 'steam_official_api'
    df['ingested_at'] = datetime.now().isoformat()
    
    # 5. Handle Storage Path
    output_dir = Path(DATA_RAW)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "steam_app_list.parquet"
    
    # 6. Save to Parquet
    try:
        # Using pyarrow or fastparquet as engine
        df.to_parquet(output_path, index=False, engine='pyarrow')
        final_count = len(df)
        
        print(f"📊 Summary:")
        print(f"   - Initial records: {initial_count}")
        print(f"   - Cleaned records: {final_count}")
        print(f"   - Saved to: {output_path.absolute()}")
    except Exception as e:
        print(f"❌ Error saving Parquet file: {e}")
        print("💡 Hint: Ensure 'pyarrow' or 'fastparquet' is installed via pip.")

if __name__ == "__main__":
    print("🚀 Starting Steam Data Ingestion (Stage 1)...")
    
    raw_data = fetch_steam_app_list()
    
    if raw_data:
        process_and_save_raw(raw_data)
        print("✅ Stage 1 completed successfully.")
    else:
        print("❌ Stage 1 failed.")
    
    print("🏁 Execution finished.")