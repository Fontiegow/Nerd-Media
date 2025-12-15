import streamlit as st
import requests
import json
import re

# --- Streamlit Page Setup ---
st.set_page_config(page_title="AI Game Recommender", page_icon="🎮", layout="centered")
st.title("🎮 AI Game Recommender (via OpenRouter)")

# --- Inputs ---
api_key = st.text_input("Enter your OpenRouter API key:", type="password")
user_input = st.text_area("Describe the kind of games you like:", placeholder="Example: atmospheric, story-rich RPGs")

model_name = "alibaba/tongyi-deepresearch-30b-a3b:free"

# --- Send request when button is clicked ---
if st.button("Get Game Recommendations"):
    if not api_key:
        st.error("Please enter your API key.")
    elif not user_input.strip():
        st.warning("Please describe your ideal game.")
    else:
        with st.spinner("🧠 Thinking..."):
            try:
                # --- Ask model to respond with JSON only ---
                prompt = f"""
                You are a game recommendation engine. 
                The user says: "{user_input}"

                Respond ONLY with valid JSON (no explanations, no markdown, no extra text).
                The format must be:
                [
                    {{
                        "title": "Game Name",
                        "cover": "Image URL",
                        "description": "Short description",
                        "release_date": "Month DD, YYYY",
                        "developer": "Developer Name",
                        "metacritic": 0-100,
                        "recent_reviews": "Short review summary",
                        "tags": ["Tag1", "Tag2", ...]
                    }},
                    ...
                ]
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

                    # --- Try extracting JSON from the response ---
                    json_match = re.search(r"\[.*\]", message, re.DOTALL)
                    if json_match:
                        try:
                            games = json.loads(json_match.group(0))

                            st.success("✅ Got recommendations!")
                            for g in games:
                                st.image(g["cover"], width=400)
                                st.subheader(g["title"])
                                st.markdown(f"**Developer:** {g['developer']}")
                                st.markdown(f"**Release Date:** {g['release_date']}")
                                st.markdown(f"**Metacritic:** {g['metacritic']}")
                                st.markdown(f"**Recent Reviews:** {g['recent_reviews']}")
                                st.markdown(f"**Tags:** {', '.join(g['tags'])}")
                                st.markdown(g["description"])
                                st.divider()

                        except json.JSONDecodeError:
                            st.error("⚠️ Model returned invalid JSON. Try again or change prompt wording.")
                    else:
                        st.error("⚠️ No JSON detected in model response.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Request failed: {str(e)}")
