import streamlit as st

st.set_page_config(
    page_title="Data Engineering Portfolio",
    layout="wide"
)

st.title("📊 My Data Engineering Portfolio")
st.subheader("Welcome to my interactive showcase")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Projects", "Dashboards", "About Me"]
)

if menu == "Home":
    st.write("Welcome to my portfolio. Explore my work using the sidebar.")

elif menu == "Projects":
    st.header("🚀 Projects")
    st.write("List your Streamlit / NiFi / PostgreSQL / ETL projects here.")

elif menu == "Dashboards":
    st.header("📈 Dashboards")
    st.write("Add charts and analytics here.")

elif menu == "About Me":
    st.header("👨‍💻 About Me")
    st.write("Data Engineering student passionate about pipelines, ETL, and cloud systems.")
