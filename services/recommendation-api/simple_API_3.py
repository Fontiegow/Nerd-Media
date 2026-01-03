import requests
import random
import time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SEARCH_URL = "https://store.steampowered.com/search/"
REVIEWS_URL = "https://store.steampowered.com/appreviews/{}"

MAX_GAMES = 1000
REVIEWS_PER_GAME = 10
OUTPUT_FILE = "steam_scraped_games.csv"


def collect_app_ids(pages=50):
    app_ids = set()

    for page in range(1, pages + 1):
        params = {"page": page}
        r = requests.get(SEARCH_URL, params=params, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        rows = soup.select("a.search_result_row")
        for row in rows:
            appid = row.get("data-ds-appid")
            if appid:
                app_ids.add(appid)

        time.sleep(0.5)

    return list(app_ids)


def scrape_game_page(appid):
    url = f"https://store.steampowered.com/app/{appid}/"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    name = soup.select_one("div.apphub_AppName")
    release = soup.select_one("div.release_date div.date")
    price = soup.select_one("div.game_purchase_price")

    return {
        "appid": appid,
        "name": name.text.strip() if name else None,
        "release_date": release.text.strip() if release else None,
        "price": price.text.strip() if price else "Free / N/A"
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


def main():
    print("Collecting app IDs...")
    app_ids = collect_app_ids(pages=60)
    random.shuffle(app_ids)
    selected_ids = app_ids[:MAX_GAMES]

    rows = []

    for appid in tqdm(selected_ids):
        try:
            game = scrape_game_page(appid)
            reviews = scrape_reviews(appid, REVIEWS_PER_GAME)

            for review in reviews:
                rows.append({
                    **game,
                    "review_text": review.get("review"),
                    "recommended": review.get("voted_up"),
                    "votes_up": review.get("votes_up")
                })

            time.sleep(0.4)

        except Exception as e:
            print(f"Failed {appid}: {e}")

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\nSaved {len(df)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
