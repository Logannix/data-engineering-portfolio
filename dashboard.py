import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Supplier Analytics Dashboard", layout="wide")

# Gemini Client (NEW SDK - correct way)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

MODEL_NAME = "models/gemini-2.5-flash"

# ---------------- ROLE ----------------
role = st.sidebar.selectbox("Login As", ["Admin", "Gamma", "User"])

st.title("Supplier Analytics Dashboard")

# ---------------- FILTERS ----------------
st.sidebar.header("Filters")

branch = st.sidebar.multiselect("Branch", ["Nairobi", "Mombasa", "Kisumu"])
item_class = st.sidebar.multiselect("Item Class", ["Class A", "Class B"])
rep_name = st.sidebar.multiselect("Rep Name", ["Kevin", "John"])
route = st.sidebar.multiselect("Route", ["North", "South"])

# ---------------- DATA ----------------
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [1200, 1800, 1500, 2100, 2600, 3000],
    "Stock": [500, 450, 420, 390, 410, 380],
    "Orders": [45, 62, 51, 73, 88, 95],
    "Branch": ["Nairobi", "Mombasa", "Nairobi", "Kisumu", "Mombasa", "Nairobi"],
    "Item Class": ["Class A", "Class B", "Class A", "Class B", "Class A", "Class B"],
    "Rep Name": ["Kevin", "John", "Kevin", "John", "Kevin", "John"],
    "Route": ["North", "South", "North", "South", "North", "South"]
})

# ---------------- FILTER LOGIC ----------------
filtered_df = df.copy()

if branch:
    filtered_df = filtered_df[filtered_df["Branch"].isin(branch)]
if item_class:
    filtered_df = filtered_df[filtered_df["Item Class"].isin(item_class)]
if rep_name:
    filtered_df = filtered_df[filtered_df["Rep Name"].isin(rep_name)]
if route:
    filtered_df = filtered_df[filtered_df["Route"].isin(route)]

# ---------------- KPI ----------------
st.subheader("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", filtered_df["Sales"].sum())
col2.metric("Avg Stock", round(filtered_df["Stock"].mean(), 2))
col3.metric("Total Orders", filtered_df["Orders"].sum())
col4.metric("Records", len(filtered_df))

# ---------------- CHARTS ----------------
st.subheader("Analytics")

st.plotly_chart(px.bar(filtered_df, x="Month", y="Sales", color="Branch"), use_container_width=True)
st.plotly_chart(px.line(filtered_df, x="Month", y="Sales", color="Branch"), use_container_width=True)
st.plotly_chart(px.area(filtered_df, x="Month", y="Orders", color="Branch"), use_container_width=True)
st.plotly_chart(px.scatter(filtered_df, x="Orders", y="Sales", color="Branch", size="Sales"), use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("Data Table")

st.dataframe(filtered_df, use_container_width=True)

st.download_button(
    "Download CSV",
    filtered_df.to_csv(index=False),
    "supplier_data.csv"
)

# ---------------- AI FUNCTION ----------------
def ask_ai(prompt, data):
    system_prompt = f"""
You are a senior business data analyst.

Analyze the dataset and explain insights clearly.

DATA:
{data.to_csv(index=False)}

QUESTION:
{prompt}

Provide:
- Key insights
- Trends
- Risks
- Opportunities
- Recommendations
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=system_prompt
    )

    return response.text

# ---------------- AI SECTION ----------------
st.subheader("AI Analysis")

if role in ["Admin", "Gamma"]:

    prompt = st.text_area("Ask a question about your data", key="ai_input")

    if st.button("Analyze", key="ai_btn"):

        if prompt:
            try:
                result = ask_ai(prompt, filtered_df)
                st.success("AI Analysis Complete")
                st.write(result)

            except Exception as e:
                st.error(f"AI Error: {e}")

else:
    st.warning("User role has no AI access")

# ---------------- ROLE INFO ----------------
st.sidebar.markdown("---")

if role == "Admin":
    st.success("Admin: Full Access")
elif role == "Gamma":
    st.info("Gamma: Dashboard + AI Access")
else:
    st.warning("User: View + Download Only")