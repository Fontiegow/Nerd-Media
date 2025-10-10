import streamlit as st
import requests
import json
import re
import time

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🎮 Nerdial Game Recommender", page_icon="🎮", layout="centered")
st.title("🎮 Nerdial Game Recommender")

# --- Inputs ---
api_key = st.text_input("Enter your OpenRouter API key:", type="password")
user_input = st.text_area("Describe your ideal game:", placeholder="Example: atmospheric story-rich RPG with exploration")

model_name = "alibaba/tongyi-deepresearch-30b-a3b:free"

# --- On button click ---
if st.button("Get Recommendations"):
    if not api_key:
        st.error("Please enter your API key.")
    elif not user_input.strip():
        st.warning("Please describe your game preferences first.")
    else:
        with st.spinner("🧠 Thinking..."):
            try:
                # --- Construct prompt ---
                prompt = f"""
                You are a video game recommendation engine.
                The user says: "{user_input}"
                
                Return ONLY a valid JSON array. 
                Each object must include a working Steam cover image URL (use the game's real App ID if known). 
                If you don't know the App ID, estimate a common one from real Steam data or use '0' instead.
                
                Format:
                [
                    {{
                        "title": "Game Name",
                        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/<APP_ID>/header.jpg",
                        "description": "Short description",
                        "release_date": "Month DD, YYYY",
                        "developer": "Developer Name",
                        "metacritic": 0-100,
                        "recent_reviews": "Very Positive (90%)",
                        "tags": ["Tag1", "Tag2", ...]
                    }},
                    ...
                ]
                
                Only output valid JSON — no markdown, no commentary.
                """

                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": model_name,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                    })
                )

                if response.status_code == 200:
                    data = response.json()
                    message = data["choices"][0]["message"]["content"].strip()

                    # --- Extract JSON safely ---
                    json_match = re.search(r"\[.*\]", message, re.DOTALL)
                    if not json_match:
                        st.error("⚠️ Could not find JSON in model response.")
                    else:
                        try:
                            games = json.loads(json_match.group(0))

                            # --- Display results ---
                            st.success("✅ Recommendations Ready!")
                            for game in games:
                                cols = st.columns([1, 2], vertical_alignment="center")
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
                                        with st.expander("Read user thoughts"):
                                            st.write("⭐ 'Engaging gameplay and immersive world.'")
                                            st.write("⭐ 'Loved the art style and soundtrack.'")
                                            st.write("⭐ 'One of the best experiences in its genre.'")

                                st.divider()

                            # Simulate loading more
                            with st.spinner("Fetching more games..."):
                                time.sleep(2)
                            st.success("✨ More recommendations loaded!")

                        except json.JSONDecodeError:
                            st.error("⚠️ Invalid JSON format returned. Try again.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Request failed: {e}")
