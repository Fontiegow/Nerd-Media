import streamlit as st
import requests
from bs4 import BeautifulSoup
from recommender import recommend_games
# from db import save_feedback

# Target URL (Steam Top Sellers page)
URL = "https://store.steampowered.com/search/?filter=topsellers"

def get_top_games(url=URL, limit=10):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    games = []
    for game_row in soup.select(".search_result_row")[:limit]:
        title = game_row.select_one(".title").text.strip() if game_row.select_one(".title") else "Unknown"
        
        # Genres are in the <div class="search_tags"> inside <a> tags
        genre_tags = [g.text.strip() for g in game_row.select(".search_tags a")]
        genres = ", ".join(genre_tags) if genre_tags else "No genre info"
        
        img = game_row.find("img")["src"] if game_row.find("img") else None

        games.append({
            "title": title,
            "genres": genres,
            "cover": img
        })
    return games


st.title("🎮 Nerd Media – Game Recommender")

user_input = st.text_input("Describe your ideal game:")

if st.button("Get Recommendations"):
    if user_input.strip():
        recs = recommend_games(user_input)
        st.subheader("Recommended Games:")
        for r in recs:
            st.write(f"- {r}")

        # Store in MongoDB
        # save_feedback(user_input, recs)

st.title("Steam Top-Selling Games")

st.write("Fetching top-selling games from Steam...")
games = get_top_games()

for g in games:
    st.image(g["cover"], width=200)
    st.write(f"**{g['title']}** — {g['genres']}")
    