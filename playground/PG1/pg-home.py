import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests

st.title("🏠 Home – Welcome to Nerdial Playground")

# Load Lottie animation
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json"
lottie_json = load_lottie(lottie_url)
if lottie_json:
    st_lottie(lottie_json, height=300)

st.markdown("""
Welcome to the Nerdial Playground test app!
- Explore games
- Filter by tags, Metacritic, multiplayer
- Watch trailers directly
- Track which games you’ve seen
""")
