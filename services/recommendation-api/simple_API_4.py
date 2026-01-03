import requests
import random
import time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from langdetect import detect, LangDetectException

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SEARCH_URL = "https://store.steampowered.com/search/"
REVIEWS_URL = "https://store.steampowered.com/appreviews/{}"

MAX_GAMES = 10000
REVIEWS_PER_GAME = 50
OUTPUT_FILE = "steam_games_reviews_en.csv"


def collect_app_ids(pages=50):
    print(f"[INFO] Collecting app IDs from {pages} Steam search pages...")
    app_ids = set()

    for page in range(1, pages + 1):
        print(f"[SEARCH] Page {page}")
        params = {"page": page}
        r = requests.get(SEARCH_URL, params=params, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        rows = soup.select("a.search_result_row")
        for row in rows:
            appid = row.get("data-ds-appid")
            if appid:
                app_ids.add(appid)

        time.sleep(0.5)

    print(f"[INFO] Collected {len(app_ids)} unique app IDs\n")
    return list(app_ids)


def scrape_game_page(appid):
    url = f"https://store.steampowered.com/app/{appid}/"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    # Skip DLC / packs
    if soup.select_one("div.game_area_dlc_bubble"):
        print(f"[SKIP] App {appid} is DLC / pack")
        return None

    name = soup.select_one("div.apphub_AppName")
    release = soup.select_one("div.release_date div.date")

    if not name:
        print(f"[SKIP] App {appid} has no game name")
        return None

    return {
        "appid": appid,
        "name": name.text.strip(),
        "release_date": release.text.strip() if release else None
    }


def scrape_reviews(appid, count):
    params = {
        "json": 1,
        "language": "english",
        "num_per_page": count,
        "filter": "random"
    }

    r = requests.get(REVIEWS_URL.format(appid), params=params, headers=HEADERS)
    data = r.json()
    return data.get("reviews", [])


def is_english(text):
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False


def main():
    print("[START] Steam review scraper started\n")

    app_ids = collect_app_ids(pages=60)
    random.shuffle(app_ids)
    selected_ids = app_ids[:MAX_GAMES]

    print(f"[INFO] Processing up to {len(selected_ids)} games\n")

    rows = []
    processed_games = 0

    for appid in tqdm(selected_ids, desc="Scraping games"):
        try:
            game = scrape_game_page(appid)
            if not game:
                continue

            reviews = scrape_reviews(appid, REVIEWS_PER_GAME)

            valid_reviews = 0

            for review in reviews:
                text = review.get("review", "")
                if not text or not is_english(text):
                    continue

                rows.append({
                    "appid": game["appid"],
                    "name": game["name"],
                    "release_date": game["release_date"],
                    "review_text": text,
                    "recommended": review.get("voted_up"),
                    "votes_up": review.get("votes_up")
                })

                valid_reviews += 1

            if valid_reviews > 0:
                processed_games += 1
                print(f"[OK] {game['name']} — {valid_reviews} English reviews kept")

            time.sleep(0.4)

        except Exception as e:
            print(f"[ERROR] App {appid} failed: {e}")

    print(f"\n[INFO] Finished scraping")
    print(f"[INFO] Valid games collected: {processed_games}")
    print(f"[INFO] Total review rows: {len(rows)}")

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"[SAVED] Dataset written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
