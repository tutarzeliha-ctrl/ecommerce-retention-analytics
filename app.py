import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce Retention & Churn Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 E-Commerce Customer Retention & Churn Analytics")
st.markdown("Modern Data Stack (dbt + Python + ML) Interactive Dashboard")

# Load Mock Datamart Data
@st.cache_data
def load_data():
    data = {
        "customer_id": [101, 102, 103, 104, 105, 106, 107, 108],
        "age": [29, 42, 35, 50, 23, 31, 45, 38],
        "total_orders": [12, 2, 15, 1, 8, 3, 20, 4],
        "lifetime_value_ltv": [5200, 450, 6800, 120, 2900, 890, 8100, 1100],
        "rfm_segment": ["Champions", "At Risk", "Champions", "Lost", "Loyal Customers", "At Risk", "Champions", "Loyal Customers"],
        "churn_probability": [0.05, 0.82, 0.03, 0.95, 0.20, 0.75, 0.02, 0.40]
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar Filters
st.sidebar.header("🎯 Filter Options")
selected_segment = st.sidebar.multiselect(
    "Select RFM Segment:",
    options=df["rfm_segment"].unique(),
    default=df["rfm_segment"].unique()
)

filtered_df = df[df["rfm_segment"].isin(selected_segment)]

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", len(filtered_df))
col2.metric("Avg Lifetime Value ($)", f"${filtered_df['lifetime_value_ltv'].mean():,.2f}" if len(filtered_df) > 0 else "$0")
col3.metric("Avg Orders", f"{filtered_df['total_orders'].mean():.1f}" if len(filtered_df) > 0 else "0")
col4.metric("Avg Churn Risk", f"{filtered_df['churn_probability'].mean()*100:.1f}%" if len(filtered_df) > 0 else "0%")

st.divider()

# Charts Section
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 LTV Distribution by Segment")
    fig_ltv = px.bar(
        filtered_df, 
        x="rfm_segment", 
        y="lifetime_value_ltv", 
        color="rfm_segment",
        title="Average LTV per RFM Segment"
    )
    st.plotly_chart(fig_ltv, use_container_width=True)

with col_right:
    st.subheader("⚠️ Churn Probability vs Total Orders")
    fig_churn = px.scatter(
        filtered_df, 
        x="total_orders", 
        y="churn_probability", 
        color="rfm_segment",
        size="lifetime_value_ltv",
        hover_data=["customer_id"]
    )
    st.plotly_chart(fig_churn, use_container_width=True)

# Data Table
st.subheader("📋 Customer Data Mart Explorer")
st.dataframe(filtered_df, use_container_width=True)