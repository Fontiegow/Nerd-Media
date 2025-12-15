import streamlit as st
from streamlit_card import card
import urllib.parse

st.set_page_config(page_title="🎮 Nerdial", layout="wide")
st.title("🎮 Nerdial")

filtered_games = [
    {
        "title": "Hollow Knight",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",
        "description": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes.",
        "release_date": "Feb 24, 2017",
        "developer": "Team Cherry",
        "metacritic": 87,
        "recent_reviews": "Overwhelmingly Positive (95%)",
        "tags": ["Metroidvania", "Souls-like", "Platformer", "Indie"]
    },
    {
        "title": "Celeste",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/504230/header.jpg",
        "description": "Help Madeline survive her journey to the top.",
        "release_date": "Jan 25, 2018",
        "developer": "Maddy Makes Games",
        "metacritic": 92,
        "recent_reviews": "Overwhelmingly Positive (97%)",
        "tags": ["Platformer", "Indie", "Pixel Graphics"]
    }
]

# --- Check if user clicked on a card (via ?game= query param)
params = st.query_params
if "game" in params:
    selected = params["game"]
    game = next((g for g in filtered_games if g["title"] == selected), None)
    if game:
        st.subheader(game["title"])
        st.image(game["cover"])
        st.write(f"**Developer:** {game['developer']}")
        st.write(f"**Release Date:** {game['release_date']}")
        st.metric("Metacritic", f"{game['metacritic']} / 100")
        st.write("**Tags:**", ", ".join(game["tags"]))
        st.write(game["description"])
    st.stop()

# --- Otherwise show list of cards
if filtered_games:
    st.subheader("🎲 Recommended Games")
    rows = [filtered_games[:3], filtered_games[3:]]
    for row in rows:
        cols = st.columns(3)
        for i, game in enumerate(row):
            with cols[i]:
                query = urllib.parse.quote(game["title"])
                card(
                    title=game["title"],
                    text=game["description"],
                    image=game["cover"],
                    url=f"?game={query}",  # click → sets query param
                    styles={
                        "card": {"width": "380px", "height": "450px", "border-radius": "12px"},
                        "img": {"object-fit": "cover", "height": "200px"},
                        "text": {"font-size": "0.8rem"}
                    }
                )
