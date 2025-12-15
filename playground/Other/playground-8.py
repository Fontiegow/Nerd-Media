import streamlit as st
from streamlit_card import card

st.set_page_config(page_title="🎮 Game Explorer", layout="wide")
st.title("🎮 Nerdial Playground")

# --- Example Game Data ---
games = [
    {
        "title": "Hollow Knight",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",
        "description": "Forge your own path in Hollow Knight!",
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
    },
    {
        "title": "The Witcher 3",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg",
        "description": "A story-driven open world RPG.",
        "release_date": "May 18, 2015",
        "developer": "CD PROJEKT RED",
        "metacritic": 93,
        "recent_reviews": "Very Positive (91%)",
        "tags": ["RPG", "Open World", "Story Rich"]
    },
    {
        "title": "Hades",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1145360/header.jpg",
        "description": "Battle out of hell in this rogue-like dungeon crawler.",
        "release_date": "Sep 17, 2020",
        "developer": "Supergiant Games",
        "metacritic": 93,
        "recent_reviews": "Overwhelmingly Positive (98%)",
        "tags": ["Rogue-like", "Action", "Indie"]
    },
    {
        "title": "Elden Ring",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg",
        "description": "A vast world full of peril and discovery awaits.",
        "release_date": "Feb 24, 2022",
        "developer": "FromSoftware Inc.",
        "metacritic": 94,
        "recent_reviews": "Very Positive (89%)",
        "tags": ["Souls-like", "Open World", "RPG"]
    },
    {
        "title": "Stardew Valley",
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/413150/header.jpg",
        "description": "Build the farm of your dreams.",
        "release_date": "Feb 26, 2016",
        "developer": "ConcernedApe",
        "metacritic": 89,
        "recent_reviews": "Overwhelmingly Positive (97%)",
        "tags": ["Farming Sim", "Casual", "Relaxing"]
    }
]

# --- Display 6 Cards (2x3 layout) ---
clicked_index = None
rows = [games[:3], games[3:]]  # split into 2 rows

for row in rows:
    cols = st.columns(3)
    for i, game in enumerate(row):
        with cols[i]:
            if card(
                title=game["title"],
                text=game["description"],
                image=game["cover"],
                url=None,
                styles={
                    "card": {"width": "270px", "height": "350px", "border-radius": "12px"},
                    "img": {"object-fit": "cover", "height": "200px"},
                    "text": {"font-size": "0.8rem"}
                }
            ):
                clicked_index = games.index(game)

# --- Detail view if clicked ---
if clicked_index is not None:
    game = games[clicked_index]

    st.markdown("---")
    cols = st.columns([1, 2])  # Image left, details right

    with cols[0]:
        st.image(game["cover"], use_container_width=True)

    with cols[1]:
        st.subheader(game["title"])
        st.write(f"**Developer:** {game['developer']}")
        st.write(f"**Release Date:** {game['release_date']}")

        # Quick metrics
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Metacritic", f"{game['metacritic']} / 100")
        with m2:
            st.metric("Recent Reviews", game["recent_reviews"])

        # Tabs for details
        tab1, tab2, tab3 = st.tabs(["📖 Description", "🔖 Tags", "💬 Reviews"])

        with tab1:
            st.write(game["description"])

        with tab2:
            st.write(", ".join(game["tags"]))

        with tab3:
            with st.expander("Read recent reviews"):
                st.write("⭐ 'Amazing exploration and combat, 10/10'")
                st.write("⭐ 'The art and music are incredible.'")
                st.write("⭐ 'Tough but fair difficulty curve.'")
