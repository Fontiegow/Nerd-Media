import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI  # OpenRouter uses the same OpenAI client interface

# Load environment variables from .env
load_dotenv()
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")  # your OpenRouter key

# Initialize client
client = OpenAI(api_key=OPENROUTER_KEY)  # just pass OpenRouter key here

st.title("🎮 Game Recommender AI")

# User input
user_input = st.text_area("Tell me what kind of games you like:")

if st.button("Get Recommendations"):
    if user_input.strip():
        with st.spinner("Thinking... 🎲"):
            prompt = (
                f"Recommend 5 video games based on this description: {user_input}. "
                "List them clearly with short explanations."
            )

            # Chat completion request
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # OpenRouter supports OpenAI models
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that recommends video games."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            # Extract response
            recommendations = response.choices[0].message.content
            st.subheader("🎯 Recommended Games")
            st.write(recommendations.strip())
    else:
        st.warning("Please describe the type of games you like.")
