import streamlit as st
from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Use a model available on free API
client = InferenceClient(model="google/flan-t5-large", token=HF_TOKEN)

st.title("🎮 Game Recommender AI")

user_input = st.text_area("Tell me what kind of games you like:")

if st.button("Get Recommendations"):
    if user_input.strip():
        with st.spinner("Thinking... 🎲"):
            prompt = f"Recommend 5 video games based on this description: {user_input}. List them clearly."
            
            response = client.text_generation(
                prompt,
                max_new_tokens=200,
                temperature=0.7
            )
        st.subheader("🎯 Recommended Games")
        st.write(response.strip())
    else:
        st.warning("Please describe the type of games you like.")
