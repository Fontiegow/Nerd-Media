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
        link = game_row["href"]

        genre_tags = [g.text.strip() for g in game_row.select(".search_tags a")]
        genres = ", ".join(genre_tags) if genre_tags else "No genre info"

        img = game_row.find("img")["src"] if game_row.find("img") else None

        release_date = game_row.select_one(".search_released")
        release_date = release_date.text.strip() if release_date else "Unknown"

        discount_pct = game_row.select_one(".search_discount span")
        discount_pct = discount_pct.text.strip() if discount_pct else "No discount"

        price = game_row.select_one(".search_price")
        price = price.text.strip() if price else "Free or Unknown"

        platforms = [p["class"][1] for p in game_row.select(".search_name .platform_img")]

        review = game_row.select_one(".search_review_summary")
        review = review["data-tooltip-html"] if review else "No reviews"

        games.append({
            "title": title,
            "link": link,
            "genres": genres,
            "cover": img,
            "release_date": release_date,
            "discount": discount_pct,
            "price": price,
            "platforms": platforms,
            "review": review
        })
    return games

def get_game_details(game_url):
    response = requests.get(game_url)
    soup = BeautifulSoup(response.text, "html.parser")

    desc = soup.select_one(".game_description_snippet")
    desc = desc.text.strip() if desc else "No description"

    recent_reviews = soup.select_one("div.user_reviews_summary_row:nth-of-type(1) .game_review_summary")
    recent_reviews = recent_reviews.text.strip() if recent_reviews else "No recent reviews"

    all_reviews = soup.select_one("div.user_reviews_summary_row:nth-of-type(2) .game_review_summary")
    all_reviews = all_reviews.text.strip() if all_reviews else "No overall reviews"

    tags = [t.text.strip() for t in soup.select(".glance_tags.popular_tags a.app_tag")]

    header = soup.select_one("#gameHeaderImageCtn img")
    header_img = header["src"] if header else None

    about = soup.select_one("#game_area_description")
    about_html = about.decode_contents() if about else "No detailed description"

    return {
        "description": desc,
        "recent_reviews": recent_reviews,
        "all_reviews": all_reviews,
        "tags": tags,
        "header_img": header_img,
        "about_html": about_html
    }



st.title("🎮 Nerdial – a Social Network for Nerds")

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
    col1, col2 = st.columns([1,3])
    with col1:
        st.image(g["cover"], width=120)
    with col2:
        st.markdown(f"### [{g['title']}]({g['link']})")
        st.write(f"**Genres:** {g['genres']}")
        st.write(f"**Release Date:** {g['release_date']}")
        st.write(f"**Price:** {g['price']} ({g['discount']})")
        st.write(f"**Review:** {g['review']}")

        # Expander for details
        with st.expander("Show more details"):
            details = get_game_details(g["link"])
            if details["header_img"]:
                st.image(details["header_img"], use_container_width=True)

            st.write(f"**Short description:** {details['description']}")
            st.write(f"**Recent reviews:** {details['recent_reviews']}")
            st.write(f"**All reviews:** {details['all_reviews']}")
            st.write(f"**Tags:** {', '.join(details['tags'])}")

            # Show full HTML description
            st.markdown("### About this game")
            st.markdown(details["about_html"], unsafe_allow_html=True)
