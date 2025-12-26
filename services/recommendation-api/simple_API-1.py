import requests

APP_ID = 620  # Portal 2


def fetch_game_details(app_id: int):
    url = "https://store.steampowered.com/api/appdetails"
    params = {
        "appids": app_id,
        "l": "english"
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()
    app_data = data[str(app_id)]

    if not app_data["success"]:
        raise ValueError("Failed to fetch app details")

    return app_data["data"]


def fetch_reviews(app_id: int, limit: int = 5):
    url = f"https://store.steampowered.com/appreviews/{app_id}"
    params = {
        "json": 1,
        "language": "english",
        "num_per_page": limit,
        "review_type": "all"
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()
    return data["reviews"]


if __name__ == "__main__":
    details = fetch_game_details(APP_ID)
    reviews = fetch_reviews(APP_ID)

    print("TITLE:")
    print(details["name"])
    print()

    print("DESCRIPTION:")
    print(details["short_description"])
    print()

    print("REVIEWS:")
    for i, review in enumerate(reviews, 1):
        print(f"{i}. {review['review'][:300]}...")
        print("-" * 40)
