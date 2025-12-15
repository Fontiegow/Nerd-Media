import streamlit as st
from streamlit_card import card
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import altair as alt

st.set_page_config(page_title="🎮 Game Explorer", layout="wide")
st.title("🎮 Interactive Game Explorer")

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
rows = [games[:3], games[3:]]  # 2 rows

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
                    "card": {
                        "width": "270px",     # narrower frame
                        "height": "350px",    # taller look
                        "border-radius": "12px",
                        "overflow": "hidden",
                    },
                    "img": {
                        "object-fit": "cover",  # crops image instead of stretching
                        "height": "200px",      # dedicate top area for cover
                    },
                    "text": {
                        "font-size": "0.8rem",
                    }
                }
            ):
                clicked_index = games.index(game)


# --- Show details if a card was clicked ---
if clicked_index is not None:
    game = games[clicked_index]
    st.subheader(f"📖 {game['title']} – Details")

    df = pd.DataFrame([{
        "Title": game["title"],
        "Release Date": game["release_date"],
        "Developer": game["developer"],
        "Metacritic": game["metacritic"],
        "Recent Reviews": game["recent_reviews"],
        "Tags": ", ".join(game["tags"])
    }])

    with st.expander("📊 Game Data", expanded=True):
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(resizable=True, filterable=True, sortable=True)
        grid_options = gb.build()
        AgGrid(df, gridOptions=grid_options, theme="streamlit", height=150, fit_columns_on_grid_load=True)

    st.subheader("📈 Tags Visualization")
    tags_df = pd.DataFrame({"Tag": game["tags"], "Count": [1]*len(game["tags"])})
    chart = alt.Chart(tags_df).mark_bar().encode(
        x="Tag",
        y="Count",
        tooltip=["Tag"]
    )
    st.altair_chart(chart, use_container_width=True)
