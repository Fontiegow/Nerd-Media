import streamlit as st
from streamlit_card import card
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import altair as alt

st.set_page_config(page_title="Interactive Streamlit Demo", layout="wide")

st.title("🚀 Polished Streamlit Components Demo")

# --- Cards Section ---
st.subheader("Choose a Dataset")
col1, col2, col3 = st.columns(3)

with col1:
    clicked1 = card(
        title="Iris Dataset",
        text="Classic dataset for ML beginners 🌸",
        image="https://archive.ics.uci.edu/ml/assets/MLimages/Large53.jpg",
        url=None  # No external link → stays local
    )
with col2:
    clicked2 = card(
        title="Titanic Dataset",
        text="Survival data from Titanic 🚢",
        image="https://upload.wikimedia.org/wikipedia/commons/f/fd/RMS_Titanic_3.jpg",
        url=None
    )
with col3:
    clicked3 = card(
        title="Custom Dataset",
        text="Upload your own CSV 📂",
        image="https://cdn-icons-png.flaticon.com/512/337/337946.png",
        url=None
    )

# --- Load Data Based on Selection ---
if clicked1:
    df = pd.DataFrame({
        "sepal_length": [5.1, 4.9, 4.7, 6.0],
        "sepal_width": [3.5, 3.0, 3.2, 3.4],
        "species": ["setosa", "setosa", "setosa", "versicolor"]
    })
    st.success("Loaded Iris Dataset 🌸")

elif clicked2:
    df = pd.DataFrame({
        "Name": ["Jack", "Rose", "Cal", "Molly"],
        "Age": [23, 19, 30, 54],
        "Survived": [1, 1, 0, 1]
    })
    st.success("Loaded Titanic Dataset 🚢")

elif clicked3:
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Loaded Custom Dataset 📂")
    else:
        df = None
else:
    df = None

# --- Show Data in Expander + AgGrid ---
if df is not None:
    with st.expander("📊 Explore Dataset", expanded=True):
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        grid_options = gb.build()

        AgGrid(df, gridOptions=grid_options, theme="streamlit", height=300, fit_columns_on_grid_load=True)

    # --- Tabs for Charts ---
    st.subheader("📈 Data Visualization")
    tab1, tab2 = st.tabs(["Bar Chart", "Scatter Plot"])

    with tab1:
        col_x = st.selectbox("X-axis", df.columns, index=0)
        col_y = st.selectbox("Y-axis", df.columns, index=1)
        chart = alt.Chart(df).mark_bar().encode(x=col_x, y=col_y).interactive()
        st.altair_chart(chart, use_container_width=True)

    with tab2:
        num_cols = df.select_dtypes(include=["number"]).columns
        if len(num_cols) >= 2:
            x_axis = st.selectbox("X-axis", num_cols, index=0, key="scatter_x")
            y_axis = st.selectbox("Y-axis", num_cols, index=1, key="scatter_y")
            scatter = alt.Chart(df).mark_circle(size=100).encode(
                x=x_axis, y=y_axis, tooltip=list(df.columns)
            ).interactive()
            st.altair_chart(scatter, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for scatter plot.")
