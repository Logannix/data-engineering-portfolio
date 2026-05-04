import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Supplier Analytics Dashboard",
    layout="wide"
)

# ---------------- GEMINI SETUP ----------------
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL_NAME = "gemini-2.0-flash"

# ---------------- ROLE ----------------
role = st.sidebar.selectbox(
    "Login As",
    ["Admin", "Gamma", "User"]
)

st.title("Supplier Analytics Dashboard")

# ---------------- FILTERS ----------------
st.sidebar.header("Filters")

branch = st.sidebar.multiselect(
    "Branch",
    ["Nairobi", "Mombasa", "Kisumu"]
)

item_class = st.sidebar.multiselect(
    "Item Class",
    ["Class A", "Class B"]
)

rep_name = st.sidebar.multiselect(
    "Rep Name",
    ["Kevin", "John"]
)

route = st.sidebar.multiselect(
    "Route",
    ["North", "South"]
)

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


# ---------------- KPI SECTION ----------------
st.subheader("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", filtered_df["Sales"].sum())
col2.metric("Average Stock", round(filtered_df["Stock"].mean(), 2))
col3.metric("Total Orders", filtered_df["Orders"].sum())
col4.metric("Records", len(filtered_df))

# ---------------- CHARTS ----------------
st.subheader("Analytics Dashboard")

fig1 = px.bar(filtered_df, x="Month", y="Sales", color="Branch")
st.plotly_chart(fig1, width="stretch")

fig2 = px.line(filtered_df, x="Month", y="Sales", color="Branch")
st.plotly_chart(fig2, width="stretch")

fig3 = px.area(filtered_df, x="Month", y="Orders", color="Branch")
st.plotly_chart(fig3, width="stretch")

fig4 = px.scatter(
    filtered_df,
    x="Orders",
    y="Sales",
    color="Branch",
    size="Sales"
)
st.plotly_chart(fig4, width="stretch")

# ---------------- DATA TABLE ----------------
st.subheader("Data Table")

st.dataframe(filtered_df, width="stretch")

st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="supplier_data.csv",
    mime="text/csv"
)

# ---------------- AI FUNCTION ----------------
def ask_ai(prompt, data):
    full_prompt = f"""
You are a senior supplier analytics consultant.

Analyze this supplier dataset and answer professionally.

Dataset:
{data.to_csv(index=False)}

Question:
{prompt}

Provide:
1. Key insights
2. Trends
3. Risks
4. Opportunities
5. Recommendations
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt
    )

    return response.text


# ---------------- AI SECTION ----------------
st.subheader("AI Analysis")

if role in ["Admin", "Gamma"]:

    prompt = st.text_area(
        "Ask a question about your data",
        key="ai_prompt"
    )

    if st.button("Analyze", key="analyze_btn"):

        if prompt:
            try:
                with st.spinner("Analyzing dashboard data..."):
                    result = ask_ai(prompt, filtered_df)

                st.success("Analysis Complete")
                st.write(result)

            except Exception as e:
                st.error(f"AI Error: {e}")

else:
    st.warning("User role has no AI access")

# ---------------- ROLE INFO ----------------
st.sidebar.markdown("---")

if role == "Admin":
    st.sidebar.success("Admin: Full Access")
elif role == "Gamma":
    st.sidebar.info("Gamma: Dashboard + AI Access")
else:
    st.sidebar.warning("User: View + Download Only")
