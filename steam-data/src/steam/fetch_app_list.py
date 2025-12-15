# src/steam/fetch_app_list.py (ویرایش شده)

import os
import requests
import pandas as pd
from dotenv import load_dotenv

# تنظیمات مسیرها
RAW_DATA_PATH = "data_raw"
OUTPUT_FILE = "steam_app_list.parquet"

# اندپوینت جدید (تغییر آدرس برای رفع خطای 404)
# این آدرس رایج‌تر و پایدارتر است
STEAM_APP_LIST_URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/"
USER_AGENT = "SteamAppListCrawler/1.0" 

# در این اندپوینت نیازی به API Key نیست، پس متغیرها حذف شدند.
# load_dotenv()
# STEAM_API_KEY = os.getenv("STEAM_API_KEY") 

def fetch_all_apps():
    """
    لیست کامل اپلیکیشن‌های استیم را از GetAppList/v0002 می‌گیرد.
    """
    print(f"Connecting to {STEAM_APP_LIST_URL} ...")

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    try:
        r = requests.get(
            STEAM_APP_LIST_URL,
            headers=headers,
            timeout=60 # افزایش تایم‌آوت برای لیست‌های بزرگ
        )

        r.raise_for_status() # اگر کد 4xx یا 5xx بود، خطا صادر می‌شود
        data = r.json()

        # ساختار داده: {"applist": {"apps": [{"appid": 123, "name": "Game Name"}, ...]}}
        apps_list = data.get("applist", {}).get("apps", [])

        if not apps_list:
            raise ValueError("No apps found in response or unexpected JSON structure.")

        print(f"Downloaded raw list containing {len(apps_list)} items.")
        
        # تنها ستون‌های مورد نیاز را استخراج می‌کنیم
        rows = []
        for app in apps_list:
             rows.append({
                 "app_id": app.get("appid"),
                 "name": app.get("name")
             })

        return pd.DataFrame(rows)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {r.status_code} - {e}")
        print("This API endpoint might be deprecated or requires a valid API key.")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"Network/Connection Error: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error processing data: {e}")
        return pd.DataFrame()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
        
    initial_count = len(df)
    print(f"Starting cleanup on {initial_count} records.")
    
    # 1. مطمئن شدن از اینکه app_id عددی است و نام رشته است
    df["app_id"] = pd.to_numeric(df["app_id"], errors="coerce")

    # 2. حذف رکوردهای بدون نام یا بدون app_id
    df.dropna(subset=["app_id", "name"], inplace=True)
    
    # 3. تبدیل app_id به عدد صحیح (Integer)
    df["app_id"] = df["app_id"].astype(int)

    # 4. حذف رکوردهای تکراری (بر اساس app_id)
    df.drop_duplicates(subset=["app_id"], keep="first", inplace=True)
    
    # 5. ریست ایندکس
    df.reset_index(drop=True, inplace=True)
    
    # اضافه کردن ستون‌های متا برای Stage 1
    df["source"] = "steam_official_v0002"

    final_count = len(df)
    print(f"Cleanup finished. Final count: {final_count} (Removed {initial_count - final_count} records)")
    return df

def main():
    df = fetch_all_apps()
    
    if df.empty:
        print("Data fetching failed or returned empty. Exiting.")
        return

    df_clean = clean_data(df)

    print(f"Total apps collected and cleaned: {len(df_clean)}")

    # ذخیره‌سازی داده خام در مسیر مشخص شده
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    output_path = os.path.join(RAW_DATA_PATH, OUTPUT_FILE)
    
    # Parquet به دلیل Columnar بودن و سرعت بالا در Pipeline
    df_clean.to_parquet(output_path, index=False, engine="pyarrow", compression="snappy")
    
    print(f"✅ Success! Raw App List saved to: {output_path}")
    print("\nFirst 5 rows:")
    print(df_clean.head())

if __name__ == "__main__":
    main()
    