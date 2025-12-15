import streamlit as st
import time

# Simulated data (could be replaced later with real API/crawler)
game_data_list = [
    {
        "title": "Hollow Knight",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",
        "description": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes.",
        "release_date": "Feb 24, 2017",
        "developer": "Team Cherry",
        "metacritic": 87,
        "recent_reviews": "Overwhelmingly Positive (95%)",
        "tags": ["Metroidvania", "Souls-like", "Platformer", "Indie"],
        "multiplayer": False,
        "free_to_play": False
    },
    {
        "title": "Dota 2",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/570/header.jpg",
        "description": "Dota 2 is a competitive game of action and strategy, played both professionally and casually by millions of players worldwide.",
        "release_date": "Jul 9, 2013",
        "developer": "Valve",
        "metacritic": 90,
        "recent_reviews": "Very Positive (91%)",
        "tags": ["MOBA", "Strategy", "Multiplayer", "eSports"],
        "multiplayer": True,
        "free_to_play": True
    }
]

# --- UI ---
st.title("🎮 Nerdial Playground – Interactive Demo")

# --- Sidebar / Filters ---
st.sidebar.header("Search & Filters")

user_input = st.sidebar.text_input("Describe your ideal game:", "")

# Collect all unique tags from sample data
all_tags = sorted({tag for g in game_data_list for tag in g["tags"]})
selected_tags = st.sidebar.multiselect("Filter by Tags:", all_tags)

min_score = st.sidebar.slider("Minimum Metacritic Score", 0, 100, 0, 1)

only_multiplayer = st.sidebar.checkbox("Only Multiplayer")
only_free = st.sidebar.checkbox("Only Free-to-Play")

# --- Simulate Recommendation / Filtering ---
if st.sidebar.button("Get Recommendations") or st.sidebar.button("Surprise Me"):
    filtered_games = []
    for g in game_data_list:
        # Text match simulation
        if user_input.lower() not in g["title"].lower() and user_input.strip() != "":
            continue
        # Tags filter
        if selected_tags and not any(tag in g["tags"] for tag in selected_tags):
            continue
        # Score filter
        if g["metacritic"] < min_score:
            continue
