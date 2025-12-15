import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_tags import st_tags
from streamlit_player import st_player
import requests

st.set_page_config(page_title="🎮 Nerdial Playground", layout="wide")

# --- Helper to load Lottie ---
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Page Title ---
st.title("🎮 Nerdial Playground – Mini Demo")

# --- Lottie Animation ---
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_puciaact.json"  # fun gamepad animation
lottie_json = load_lottie(lottie_url)
if lottie_json:
    st_lottie(lottie_json, height=250, key="intro")

st.subheader("Pick your favorite game genres:")

# --- Tags input ---
tags = st_tags(
    label="🎯 Select or add tags:",
    text="Press enter to add more",
    value=["Action", "Adventure"],
    suggestions=["RPG", "Shooter", "Indie", "MOBA", "Metroidvania", "Simulation"],
    maxtags=6,
    key="1",
)

st.write("You picked:", ", ".join(tags) if tags else "No tags yet")

# --- Player ---
st.subheader("Featured Trailer")
st_player("https://www.youtube.com/watch?v=UAO2urG23S4")  # Hollow Knight trailer

# --- Fake Recommendation Based on Tags ---
if tags:
    st.success(f"Because you like {', '.join(tags)}, you might enjoy **Hollow Knight** 🦋")
