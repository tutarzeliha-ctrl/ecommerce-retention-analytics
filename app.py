import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="E-Commerce Retention & Churn Analytics",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 E-Commerce Retention, LTV & Churn Analytics Pipeline")
st.markdown(
    "An end-to-end Modern Data Stack (MDS) & Machine Learning solution for European e-commerce platforms."
)

# Load Processed Data
df = pd.read_csv("dim_customers_mart.csv")

# ---------------------------------------------------------
# TOP METRICS (KPIs)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_customers = len(df)
churn_rate = df["is_churned"].mean() * 100
avg_ltv = df["lifetime_value_ltv"].mean()
total_ltv = df["lifetime_value_ltv"].sum()

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churn Rate", f"{churn_rate:.1f}%")
col3.metric("Average LTV", f"€{avg_ltv:.2f}")
col4.metric("Total LTV", f"€{total_ltv:,.2f}")

st.divider()

# ---------------------------------------------------------
# CHARTS & ANALYTICS
# ---------------------------------------------------------
st.subheader("📊 Customer Distribution & ML Insights")

left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### Customers by Country")
    country_counts = df["country"].value_counts().reset_index()
    country_counts.columns = ["Country", "Count"]

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        data=country_counts,
        x="Country",
        y="Count",
        palette="viridis",
        ax=ax1,
        hue="Country",
        legend=False,
    )
    ax1.set_ylabel("Number of Users")
    st.pyplot(fig1)

with right_col:
    st.markdown("### Churn Status Breakdown")
    churn_counts = (
        df["is_churned"]
        .map({0: "Active", 1: "Churned"})
        .value_counts()
        .reset_index()
    )
    churn_counts.columns = ["Status", "Count"]

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        data=churn_counts,
        x="Status",
        y="Count",
        palette="mako",
        ax=ax2,
        hue="Status",
        legend=False,
    )
    ax2.set_ylabel("Number of Users")
    st.pyplot(fig2)

# ---------------------------------------------------------
# DATA TABLE EXPLORER
# ---------------------------------------------------------
st.divider()
st.subheader("🔍 Data Mart Explorer (`dim_customers_mart`)")

selected_country = st.selectbox(
    "Filter by Country:", ["All"] + list(df["country"].unique())
)

if selected_country != "All":
    filtered_df = df[df["country"] == selected_country]
else:
    filtered_df = df

st.dataframe(filtered_df, use_container_width=True)