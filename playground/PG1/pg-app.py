import streamlit as st

st.set_page_config(page_title="Nerdial Playground", layout="wide", page_icon="🎮")
st.title("🎮 Nerdial Playground – Main Menu")

st.markdown(
    """
    Use the sidebar to navigate pages:
    - Home: Welcome + recent games
    - Recommendations: Filter & explore games
    - Dashboard: Visual analytics
    """
)

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to page:", ["Home", "Recommendations", "Dashboard"])

if page == "Home":
    st.write("Go to the 'pg-home.py' for Home page.")
elif page == "Recommendations":
    st.write("Go to the 'pg-recommendations.py' for Recommendations page.")
elif page == "Dashboard":
    st.write("Go to the 'pg-dashboard.py' for Dashboard page.")
