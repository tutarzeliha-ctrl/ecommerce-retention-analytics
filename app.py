import pandas as pd
import json

print("="*50)
print("🔄 REVERSE ETL PIPELINE STARTED")
print("="*50)

# Load user and order datasets
users = pd.read_csv('raw_users.csv')
orders = pd.read_csv('raw_orders.csv')

# Identify high-risk churn customers (Simulation: Longest time since last order)
orders['order_date'] = pd.to_datetime(orders['order_date'])
last_orders = orders.groupby('user_id')['order_date'].max().reset_index()

# Select top 3 customers with oldest last order dates
churn_risk_users = last_orders.sort_values(by='order_date').head(3)
merged_risk = churn_risk_users.merge(users, on='user_id')

print(f"\n🚨 {len(merged_risk)} High Churn Risk Customers Identified!\n")

# Outbound Webhook / Slack / CRM Notification Simulation
for index, user in merged_risk.iterrows():
    slack_payload = {
        "channel": "#crm-churn-alerts",
        "username": "RetentionBot",
        "event": "HIGH_CHURN_RISK",
        "data": {
            "user_id": user['user_id'],
            "country": user['country'],
            "last_order": user['order_date'].strftime('%Y-%m-%d'),
            "action_required": "Trigger 15% Win-back Discount Coupon"
        }
    }
    print(f"📡 [Webhook Outbound] -> Slack/CRM: {json.dumps(slack_payload, ensure_ascii=False)}")

print("\n" + "="*50)
print("✅ REVERSE ETL PIPELINE COMPLETED SUCCESSFULLY")
print("="*50)