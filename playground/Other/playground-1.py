import streamlit as st

# Simulated scraped data
game_data = {
    "title": "Hollow Knight",
    "cover": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",
    "description": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes.",
    "release_date": "Feb 24, 2017",
    "developer": "Team Cherry",
    "metacritic": 87,
    "recent_reviews": "Overwhelmingly Positive (95%)",
    "tags": ["Metroidvania", "Souls-like", "Platformer", "Indie"]
}

# --- UI Layout ---
st.title("🎮 Nerdial Playground")

# Game Card Layout
cols = st.columns([1, 2])  # Image on left, details on right

with cols[0]:
    st.image(game_data["cover"], use_container_width=True)

with cols[1]:
    st.subheader(game_data["title"])
    st.write(f"**Developer:** {game_data['developer']}")
    st.write(f"**Release Date:** {game_data['release_date']}")

    # Quick metrics row
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Metacritic", f"{game_data['metacritic']} / 100")
    with m2:
        st.metric("Recent Reviews", game_data["recent_reviews"])

    # Tabs for details
    tab1, tab2, tab3 = st.tabs(["📖 Description", "🔖 Tags", "💬 Reviews"])

    with tab1:
        st.write(game_data["description"])

    with tab2:
        st.write(", ".join(game_data["tags"]))

    with tab3:
        with st.expander("Read recent reviews"):
            st.write("⭐ 'Amazing exploration and combat, 10/10'")
            st.write("⭐ 'The art and music are incredible.'")
            st.write("⭐ 'Tough but fair difficulty curve.'")

# Show loading while simulating fetch
with st.spinner("Fetching more games..."):
    import time
    time.sleep(2)

st.success("More recommendations loaded!")
