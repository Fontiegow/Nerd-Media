import streamlit as st
import pandas as pd
import time

# --- Base game data (simulate enriched Steam data) ---
game_data_list = [
    {
        "title": "Hollow Knight",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",
        "description": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes.",
        "release_date": "2017-02-24",
        "developer": "Team Cherry",
        "metacritic": 87,
        "recent_reviews": 95,  # numeric percent
        "tags": ["Metroidvania", "Souls-like", "Platformer", "Indie"],
        "multiplayer": False,
        "free_to_play": False,
        "player_count": 100000
    },
    {
        "title": "Dota 2",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/570/header.jpg",
        "description": "Dota 2 is a competitive game of action and strategy, played both professionally and casually by millions of players worldwide.",
        "release_date": "2013-07-09",
        "developer": "Valve",
        "metacritic": 90,
        "recent_reviews": 91,
        "tags": ["MOBA", "Strategy", "Multiplayer", "eSports"],
        "multiplayer": True,
        "free_to_play": True,
        "player_count": 800000
    },
    {
        "title": "Stardew Valley",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/413150/header.jpg",
        "description": "You've inherited your grandfather's farm in Stardew Valley! Manage crops, animals, and relationships in this farming sim.",
        "release_date": "2016-02-26",
        "developer": "ConcernedApe",
        "metacritic": 89,
        "recent_reviews": 97,
        "tags": ["Farming", "Simulation", "Indie", "Relaxing"],
        "multiplayer": True,
        "free_to_play": False,
        "player_count": 250000
    }
]

# Convert to DataFrame for easier filtering / visualization
df = pd.DataFrame(game_data_list)

# --- Sidebar: Filters ---
st.sidebar.header("🔍 Search & Filters")
search_text = st.sidebar.text_input("Search by title:")
selected_tags = st.sidebar.multiselect(
    "Filter by Tags:", sorted({tag for g in game_data_list for tag in g["tags"]})
)
min_metacritic = st.sidebar.slider("Minimum Metacritic Score", 0, 100, 0)
only_multiplayer = st.sidebar.checkbox("Only Multiplayer")
only_free = st.sidebar.checkbox("Only Free-to-Play")

# --- Filtering logic ---
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

st.title("🎮 Nerdial Playground – Interactive Games")

# --- Display filtered games as cards ---
for _, g in filtered_df.iterrows():
    cols = st.columns([1, 2])
    with cols[0]:
        st.image(g["cover"], use_container_width=True)
    with cols[1]:
        st.subheader(g["title"])
        st.write(f"**Developer:** {g['developer']}")
        st.write(f"**Release Date:** {g['release_date']}")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Metacritic", f"{g['metacritic']} / 100")
        with m2:
            st.metric("Recent Reviews", f"{g['recent_reviews']}%")
        st.write(f"**Player Count:** {g['player_count']:,}")
        tab1, tab2, tab3 = st.tabs(["📖 Description", "🔖 Tags", "💬 Reviews"])
        with tab1:
            st.write(g["description"])
        with tab2:
            st.write(", ".join(g["tags"]))
        with tab3:
            with st.expander("Sample review summary"):
                st.write(f"Recent reviews: {g['recent_reviews']}% positive")

    st.divider()

# --- Data Visualization ---
st.markdown("### 📊 Overview Charts")

# 1. Metacritic distribution
st.bar_chart(filtered_df[['title','metacritic']].set_index('title'))

# 2. Player count comparison
st.bar_chart(filtered_df[['title','player_count']].set_index('title'))

# 3. Optional: show full DataFrame
with st.expander("View raw data"):
    st.dataframe(filtered_df)
