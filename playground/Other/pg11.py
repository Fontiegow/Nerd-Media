import streamlit as st
import requests
import json

# --- Streamlit Page Setup ---
st.set_page_config(page_title="AI Chat via OpenRouter", page_icon="🤖", layout="centered")
st.title("💬 Chat with OpenRouter Model")

# --- User Inputs ---
api_key = st.text_input("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", type="password")
user_input = st.text_area("🗨️ Your message:", placeholder="Type something...")

# Optional settings
model_name = "alibaba/tongyi-deepresearch-30b-a3b:free"
site_url = "https://yourwebsite.com"
site_title = "My Streamlit AI Chat"

# --- Send request when button is clicked ---
if st.button("Send Message"):
    if not api_key:
        st.error("Please enter your API key.")
    elif not user_input.strip():
        st.warning("Please type a message first.")
    else:
        with st.spinner("🤔 Thinking..."):
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": model_name,
                        "messages": [{"role": "user", "content": user_input}],
                    })
                )

                if response.status_code == 200:
                    data = response.json()
                    message = data["choices"][0]["message"]["content"]
                    st.success("✅ Response received!")
                    st.markdown(f"### 🤖 Model Reply:\n{message}")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Request failed: {str(e)}")