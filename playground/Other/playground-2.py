# app.py
import re
import time
import requests
import streamlit as st

STEAM_APPDETAILS = "https://store.steampowered.com/api/appdetails"
STEAM_APPREVIEWS = "https://store.steampowered.com/appreviews/{appid}"
RAWG_SEARCH = "https://api.rawg.io/api/games"   # requires API key (optional)

# --- Helpers ---
def extract_appid_from_url(url: str):
    """Try to pull a numeric Steam appid from the product URL."""
    m = re.search(r"/app/(\d+)", url)
    if m:
        return m.group(1)
    # fallback: some pages can have data-ds-appid attributes etc. Add more heuristics if needed.
    raise ValueError("Could not extract appid from URL. Make sure it's a /app/<id>/... url.")

@st.cache_data(ttl=3600)
def fetch_appdetails(appid: str, country="us", language="en"):
    """Use the public store 'appdetails' API for structured game metadata."""
    params = {"appids": appid, "cc": country, "l": language}
    resp = requests.get(STEAM_APPDETAILS, params=params, timeout=10)
    resp.raise_for_status()
    payload = resp.json()
    if not payload or not payload.get(appid, {}).get("success"):
        return None
    return payload[appid]["data"]

@st.cache_data(ttl=600)
def fetch_recent_reviews(appid: str, day_range: int = 30, num_per_page: int = 100, language="all"):
    """
    Use the 'appreviews' endpoint to fetch recent reviews.
    We request reviews and compute % positive from the returned batch.
    """
    url = STEAM_APPREVIEWS.format(appid=appid)
    params = {
        "json": 1,
        "filter": "updated",        # try 'updated' or 'recent'
        "language": language,
        "day_range": day_range,     # recent window
        "num_per_page": num_per_page,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    j = resp.json()
    reviews = j.get("reviews", [])
    num = len(reviews)
    if num == 0:
        return {"num": 0, "positive": None, "positive_pct": None, "sample": []}
    positive = sum(1 for r in reviews if r.get("voted_up"))
    pct = 100.0 * positive / num if num else None
    # collect short sample excerpts (first 3)
    sample = []
    for r in reviews[:3]:
        sample.append({
            "text": r.get("review", "")[:300],
            "voted_up": r.get("voted_up"),
            "author": r.get("author", {}).get("steamid", "unknown"),
            "timestamp": r.get("timestamp_created"),
        })
    return {"num": num, "positive": positive, "positive_pct": pct, "sample": sample, "raw": j}

@st.cache_data(ttl=3600)
def fetch_metacritic_from_rawg(name: str, rawg_key: str = None):
    """Optional: ask RAWG for the game's metacritic score (RAWG exposes 'metacritic' field)."""
    if not rawg_key:
        return None
    params = {"search": name, "page_size": 1, "key": rawg_key}
    resp = requests.get(RAWG_SEARCH, params=params, timeout=8)
    if resp.status_code != 200:
        return None
    j = resp.json()
    results = j.get("results") or []
    if not results:
        return None
    return results[0].get("metacritic")

def enrich_game_by_url(game_url: str, rawg_key: str = None, day_range:int=30):
    """Combine appdetails + reviews + RAWG metacritic fallback into one dict."""
    try:
        appid = extract_appid_from_url(game_url)
    except ValueError:
        return {"error": "Can't parse appid"}

    details = fetch_appdetails(appid)
    if details is None:
        return {"error": "No details from Steam API for appid " + appid}

    # Basic fields
    title = details.get("name")
    cover = details.get("header_image")
    short_desc = details.get("short_description")
    release_date = details.get("release_date", {}).get("date") if isinstance(details.get("release_date"), dict) else details.get("release_date")
    developers = details.get("developers", [])
    # Player modes / features are returned under 'categories' (each item has 'description')
    player_modes = [c.get("description") for c in details.get("categories", []) if c.get("description")]

    # Steam sometimes includes a 'metacritic' block in appdetails
    meta = details.get("metacritic") or {}
    metacritic_score = meta.get("score")

    # Reviews from the appreviews endpoint (recent period)
    reviews_summary = fetch_recent_reviews(appid, day_range=day_range)

    # Fallback: RAWG metacritic if Steam didn't include it
    if metacritic_score is None and rawg_key:
        try:
            metacritic_score = fetch_metacritic_from_rawg(title, rawg_key)
        except Exception:
            metacritic_score = None

    return {
        "appid": appid,
        "title": title,
        "cover": cover,
        "short_desc": short_desc,
        "release_date": release_date,
        "developers": developers,
        "player_modes": player_modes,
        "metacritic": metacritic_score,
        "reviews_summary": reviews_summary,
        "raw_details": details
    }

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Steam Enriched Cards", layout="wide")
st.title("🎮 Steam — enriched cards (appdetails + appreviews + RAWG)")

rawg_key = st.sidebar.text_input("RAWG API Key (optional - used for Metacritic fallback)", type="password")
game_url_input = st.text_input("Paste Steam Game URL (example: https://store.steampowered.com/app/570/Dota_2/ )")

if st.button("Fetch & show"):
    if not game_url_input.strip():
        st.error("Paste a Steam URL first.")
    else:
        with st.spinner("Fetching structured data from Steam..."):
            enriched = enrich_game_by_url(game_url_input.strip(), rawg_key=rawg_key, day_range=30)
            time.sleep(0.5)  # politeness

        if enriched.get("error"):
            st.error(enriched["error"])
        else:
            cols = st.columns([1, 2])
            with cols[0]:
                if enriched["cover"]:
                    st.image(enriched["cover"], use_container_width=True)
                else:
                    st.write("No cover found")
            with cols[1]:
                st.subheader(enriched["title"])
                st.write(f"**Developer(s):** {', '.join(enriched['developers']) if enriched['developers'] else 'N/A'}")
                st.write(f"**Release Date:** {enriched['release_date'] or 'N/A'}")
                # Metacritic metric with logo (you should have 'metacritic_logo.png' in project folder)
                m1, m2 = st.columns([1, 4])
                with m1:
                    try:
                        st.image("metacritic_logo.png", width=56)
                    except Exception:
                        st.write("")  # logo optional
                with m2:
                    st.metric("Metacritic", str(enriched.get("metacritic") or "N/A"))

                # Reviews metric (computed from recent batch)
                rev = enriched["reviews_summary"]
                if rev["num"] and rev["positive_pct"] is not None:
                    st.metric("Recent positive %", f"{rev['positive_pct']:.1f}% ({rev['num']} samples)")
                else:
                    st.write("No recent review samples from API")

                st.write("**Player Modes / Categories:**", ", ".join(enriched["player_modes"]) if enriched["player_modes"] else "N/A")
                st.markdown("### Short description")
                st.write(enriched["short_desc"] or "N/A")

                with st.expander("Sample recent reviews (API excerpts)"):
                    for s in rev.get("sample", []):
                        st.write(f"- {'👍' if s['voted_up'] else '👎'} {s['text'][:300]}")

            st.divider()
            st.success("Done — structured data used (less flaky than scraping HTML).")
