import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Dashboard – Game Analytics")

# Sample data
data = {
    "title": ["Hollow Knight", "Dota 2"],
    "metacritic": [87, 90],
    "recent_reviews": [95, 91],
    "player_count": [100000, 800000]
}
df = pd.DataFrame(data)

# --- Charts ---
st.markdown("#### Metacritic Scores")
st.bar_chart(df.set_index("title")["metacritic"])

st.markdown("#### Recent Review %")
st.bar_chart(df.set_index("title")["recent_reviews"])

st.markdown("#### Player Count")
st.bar_chart(df.set_index("title")["player_count"])

with st.expander("Raw Data"):
    st.dataframe(df)
