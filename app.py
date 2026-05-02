import streamlit as st
import psycopg2

DATABASE_URL = st.secrets["DATABASE_URL"]

def get_connection():
    return psycopg2.connect(DATABASE_URL)

st.title("Neon + Streamlit Connection Test")

try:
    conn = get_connection()
    cur = conn.cursor()

    asset_name = st.text_input("Asset Name")
    category = st.text_input("Category")

    if st.button("Save Asset"):
        cur.execute(
            "INSERT INTO assets (asset_name, category) VALUES (%s, %s)",
            (asset_name, category)
        )
        conn.commit()
        st.success("Asset saved successfully!")

    cur.execute("SELECT * FROM assets ORDER BY id DESC;")
    rows = cur.fetchall()

    st.subheader("Saved Assets")
    st.dataframe(rows)

except Exception as e:
    st.error(f"Database connection failed: {e}")