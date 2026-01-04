import requests
import random
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from langdetect import detect, LangDetectException

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SEARCH_URL = "https://store.steampowered.com/search/"
REVIEWS_URL = "https://store.steampowered.com/appreviews/{}"

MAX_GAMES = 1000
REVIEWS_PER_GAME = 10

JSON_OUTPUT = "steam_games_reviews.json"
CSV_OUTPUT = "steam_games_reviews.csv"


def collect_app_ids(pages=50):
    print(f"[INFO] Collecting app IDs from {pages} pages")
    app_ids = set()

    for page in range(1, pages + 1):
        print(f"[SEARCH] Page {page}")
        r = requests.get(SEARCH_URL, params={"page": page}, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        for row in soup.select("a.search_result_row"):
            appid = row.get("data-ds-appid")
            if appid:
                app_ids.add(appid)

        time.sleep(0.5)

    print(f"[INFO] Found {len(app_ids)} unique app IDs\n")
    return list(app_ids)


def scrape_game_page(appid):
    url = f"https://store.steampowered.com/app/{appid}/"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    # Skip DLC / packs
    if soup.select_one("div.game_area_dlc_bubble"):
        print(f"[SKIP] {appid} is DLC / pack")
        return None

    name = soup.select_one("div.apphub_AppName")
    release = soup.select_one("div.release_date div.date")

    if not name:
        return None

    return {
        "appid": int(appid),
        "name": name.text.strip(),
        "release_date": release.text.strip() if release else None,
        "reviews": []
    }


def scrape_reviews(appid, count):
    r = requests.get(
        REVIEWS_URL.format(appid),
        params={
            "json": 1,
            "language": "english",
            "num_per_page": count,
            "filter": "random"
        },
        headers=HEADERS
    )
    return r.json().get("reviews", [])


def is_english(text):
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False


def main():
    print("[START] Steam semantic dataset builder\n")

    app_ids = collect_app_ids(pages=60)
    random.shuffle(app_ids)
    selected_ids = app_ids[:MAX_GAMES]

    games = []

    for appid in tqdm(selected_ids, desc="Scraping games"):
        try:
            game = scrape_game_page(appid)
            if not game:
                continue

            reviews = scrape_reviews(appid, REVIEWS_PER_GAME)

            for review in reviews:
                text = review.get("review", "")
                if not text or not is_english(text):
                    continue

                game["reviews"].append({
                    "text": text,
                    "recommended": review.get("voted_up"),
                    "votes_up": review.get("votes_up")
                })

            if game["reviews"]:
                games.append(game)
                print(f"[OK] {game['name']} — {len(game['reviews'])} reviews")

            time.sleep(0.4)

        except Exception as e:
            print(f"[ERROR] {appid}: {e}")

    print(f"\n[INFO] Writing JSON ({len(games)} games)")
    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)

    print("[INFO] Generating CSV from JSON")

    rows = []
    for game in games:
        for review in game["reviews"]:
            rows.append({
                "appid": game["appid"],
                "name": game["name"],
                "release_date": game["release_date"],
                "review_text": review["text"],
                "recommended": review["recommended"],
                "votes_up": review["votes_up"]
            })

    df = pd.DataFrame(rows)
    df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")

    print(f"[DONE] JSON saved to {JSON_OUTPUT}")
    print(f"[DONE] CSV saved to {CSV_OUTPUT}")
    print(f"[STATS] {len(games)} games | {len(df)} reviews")


if __name__ == "__main__":
    main()
