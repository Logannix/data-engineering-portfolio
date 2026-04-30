import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Portfolio", layout="wide")

# ---------------- SIDEBAR NAV ----------------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Projects", "Dashboards", "Database"]
)

# ---------------- HOME ----------------
if menu == "Home":
    st.title("📊 Data Engineering Portfolio")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Projects", "5")

    with col2:
        st.metric("Pipelines", "3")

    with col3:
        st.metric("Dashboards", "2")

# ---------------- PROJECTS ----------------
elif menu == "Projects":
    st.header("🚀 Projects")
    st.write("Your ETL, Streamlit, NiFi projects go here")

# ---------------- DASHBOARDS ----------------
elif menu == "Dashboards":
    st.header("📈 Dashboards")

    data = pd.DataFrame({
        "Project": ["ETL", "Streamlit", "NiFi"],
        "Progress": [90, 70, 80]
    })

    st.bar_chart(data.set_index("Project"))

# ---------------- DATABASE ----------------
elif menu == "Database":
    st.header("🗄️ Database Connection Layer")
    st.write("PostgreSQL integration will go here")
