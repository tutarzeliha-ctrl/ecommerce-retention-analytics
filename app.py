import streamlit as st
import pandas as pd
import json

# Streamlit Sayfa Ayarı
st.set_page_config(page_title="E-Commerce Retention & Churn Analytics", page_icon="🛒", layout="wide")

st.title("🛒 E-Commerce Retention & Churn Analytics")
st.markdown("---")
st.markdown("### 🔄 Reverse ETL Pipeline & Churn Risk Simulation")

# Load user and order datasets
@st.cache_data
def load_data():
    users = pd.read_csv('raw_users.csv')
    orders = pd.read_csv('raw_orders.csv')
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    return users, orders

users, orders = load_data()

# Identify high-risk churn customers
last_orders = orders.groupby('user_id')['order_date'].max().reset_index()
churn_risk_users = last_orders.sort_values(by='order_date').head(3)
merged_risk = churn_risk_users.merge(users, on='user_id')

# UI Metrikleri (4'lü şık sütun tasarımı)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Users", value=len(users))
with col2:
    st.metric(label="Total Orders", value=len(orders))
with col3:
    completed_orders = len(orders[orders['status'] == 'completed'])
    st.metric(label="Completed Orders", value=completed_orders)
with col4:
    st.metric(label="High Churn Risk", value=len(merged_risk))

st.markdown("---")
st.markdown("### 🚨 Identified High-Risk Churn Customers")
st.dataframe(merged_risk, use_container_width=True)

st.markdown("---")
st.markdown("### 📡 Outbound Webhook / Slack CRM Notifications")

# Outbound Webhook Simulation as UI elements
for index, user in merged_risk.iterrows():
    slack_payload = {
        "channel": "#crm-churn-alerts",
        "username": "RetentionBot",
        "event": "HIGH_CHURN_RISK",
        "data": {
            "user_id": str(user['user_id']),
            "country": str(user['country']),
            "last_order": user['order_date'].strftime('%Y-%m-%d'),
            "action_required": "Trigger 15% Win-back Discount Coupon"
        }
    }
    st.code(json.dumps(slack_payload, indent=2, ensure_ascii=False), language="json")

st.success("✅ Reverse ETL Pipeline Completed Successfully!")