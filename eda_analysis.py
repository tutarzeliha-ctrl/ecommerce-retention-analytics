import numpy as np
import pandas as pd

# Load raw datasets
users = pd.read_csv("raw_users.csv")
products = pd.read_csv("raw_products.csv")
orders = pd.read_csv("raw_orders.csv")
order_items = pd.read_csv("raw_order_items.csv")

print("--- 1. OVERALL BUSINESS METRICS ---")
# Merge order items with products to get revenue and cost
df_items = order_items.merge(products, on="product_id", how="left")
df_items["gross_revenue"] = (
    df_items["quantity"] * df_items["unit_price_x"] * (1 - df_items["discount"])
)
df_items["total_cost"] = df_items["quantity"] * df_items["unit_cost"]

# Merge with orders to filter completed orders for metrics
df_full = df_items.merge(orders, on="order_id", how="left").merge(
    users, on="user_id", how="left"
)

completed_orders = df_full[df_full["status"] == "completed"]

total_revenue = completed_orders["gross_revenue"].sum()
total_cost = completed_orders["total_cost"].sum()
net_profit = total_revenue - total_cost
profit_margin = (net_profit / total_revenue) * 100
total_orders_count = orders[orders["status"] == "completed"][
    "order_id"
].nunique()
aov = total_revenue / total_orders_count

print(f"Total Gross Revenue: ${total_revenue:,.2f}")
print(f"Net Profit: ${net_profit:,.2f} (Margin: {profit_margin:.1f}%)")
print(f"Completed Orders: {total_orders_count}")
print(f"Average Order Value (AOV): ${aov:.2f}\n")

print("--- 2. ORDER STATUS BREAKDOWN ---")
status_breakdown = orders["status"].value_counts(normalize=True) * 100
print(status_breakdown.round(2).to_string() + "%\n")

print("--- 3. REVENUE BY COUNTRY ---")
country_revenue = (
    completed_orders.groupby("country")["gross_revenue"].sum().sort_values(ascending=False)
)
print(country_revenue.round(2).to_string() + "\n")

print("--- 4. REVENUE BY ACQUISITION CHANNEL ---")
channel_revenue = (
    completed_orders.groupby("acquisition_channel")["gross_revenue"]
    .sum()
    .sort_values(ascending=False)
)
print(channel_revenue.round(2).to_string())
