import streamlit as st
from st_aggrid import AgGrid
from streamlit_tags import st_tags
from streamlit_player import st_player
from streamlit_card import card
import pandas as pd

# --- Sample game data ---
game_data_list = [
    {
        "title": "Hollow Knight",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",
        "description": "Epic action adventure through a ruined insect kingdom.",
        "release_date": "2017-02-24",
        "developer": "Team Cherry",
        "metacritic": 87,
        "recent_reviews": 95,
        "tags": ["Metroidvania", "Souls-like", "Platformer", "Indie"],
        "multiplayer": False,
        "free_to_play": False,
        "trailer": "https://www.youtube.com/watch?v=UAO2urG23S4"
    },
    {
        "title": "Dota 2",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/570/header.jpg",
        "description": "Competitive MOBA game with millions of players.",
        "release_date": "2013-07-09",
        "developer": "Valve",
        "metacritic": 90,
        "recent_reviews": 91,
        "tags": ["MOBA", "Strategy", "Multiplayer", "eSports"],
        "multiplayer": True,
        "free_to_play": True,
        "trailer": "https://www.youtube.com/watch?v=2bN9rXHzrRA"
    }
]

# --- Session state to track seen games ---
if "seen_games" not in st.session_state:
    st.session_state["seen_games"] = set()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
search_text = st.sidebar.text_input("Search by title:")
selected_tags = st_tags(label="Select Tags", text="", value=[], suggestions=[tag for g in game_data_list for tag in g["tags"]])
min_metacritic = st.sidebar.slider("Min Metacritic", 0, 100, 0)
only_multiplayer = st.sidebar.checkbox("Multiplayer Only")
only_free = st.sidebar.checkbox("Free to Play Only")

# --- Filtering ---
df = pd.DataFrame(game_data_list)
filtered_df = df.copy()

if search_text:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_text, case=False)]
if selected_tags:
    filtered_df = filtered_df[filtered_df['tags'].apply(lambda tags: any(t in tags for t in selected_tags))]
filtered_df = filtered_df[filtered_df['metacritic'] >= min_metacritic]
if only_multiplayer:
    filtered_df = filtered_df[filtered_df['multiplayer'] == True]
if only_free:
    filtered_df = filtered_df[filtered_df['free_to_play'] == True]

# --- Display using cards ---
st.title("🎮 Game Recommendations")
for _, g in filtered_df.iterrows():
    with card(title=g['title'], image=g['cover']):
        st.write(f"**Developer:** {g['developer']}")
        st.write(f"**Release Date:** {g['release_date']}")
        st.metric("Metacritic", f"{g['metacritic']} / 100")
        st.metric("Recent Reviews", f"{g['recent_reviews']}%")
        st.write("**Tags:**", ", ".join(g['tags']))
        st_player(g['trailer'])
        st.button("Mark as Seen", key=f"seen_{g['title']}", on_click=lambda t=g['title']: st.session_state['seen_games'].add(t))

st.write("Games seen:", ", ".join(st.session_state["seen_games"]))
