import pandas as pd
import numpy as np

# Load Raw Data
users_df = pd.read_csv("raw_users.csv")
orders_df = pd.read_csv("raw_orders.csv")
order_items_df = pd.read_csv("raw_order_items.csv")
products_df = pd.read_csv("raw_products.csv")

# ---------------------------------------------------------
# STAGING LAYER SIMULATION (dbt Models)
# ---------------------------------------------------------
# 1. stg_users
stg_users = users_df.copy()

# 2. stg_orders & stg_order_items (Calculate total per order item)
order_items_df["item_revenue"] = order_items_df["quantity"] * order_items_df["unit_price"] * (1 - order_items_df["discount"])
completed_orders = orders_df[orders_df["status"] == "completed"]

# Join completed items with orders
completed_items = order_items_df.merge(completed_orders, on="order_id")

# ---------------------------------------------------------
# MARTS LAYER SIMULATION (dim_customers.sql)
# ---------------------------------------------------------
# Calculate aggregated customer metrics
user_metrics = completed_items.groupby("user_id").agg(
    total_orders=("order_id", "nunique"),
    lifetime_value_ltv=("item_revenue", "sum"),
    last_order_date=("order_date", "max"),
    first_order_date=("order_date", "min")
).reset_index()

# Merge with all users to keep user-level profile
dim_customers = stg_users.merge(user_metrics, on="user_id", how="left")

# Fill NaN values for users with no completed orders
dim_customers["total_orders"] = dim_customers["total_orders"].fillna(0).astype(int)
dim_customers["lifetime_value_ltv"] = dim_customers["lifetime_value_ltv"].fillna(0.0).round(2)

# Convert order_date to datetime to calculate Recency
dim_customers["last_order_date"] = pd.to_datetime(dim_customers["last_order_date"])
max_date = pd.to_datetime("2026-07-01") # Reference analysis date

dim_customers["recency_days"] = (max_date - dim_customers["last_order_date"]).dt.days
dim_customers["recency_days"] = dim_customers["recency_days"].fillna(999).astype(int)

# Define Churn: No completed order in the last 180 days OR 0 orders
dim_customers["is_churned"] = np.where(
    (dim_customers["recency_days"] > 180) | (dim_customers["total_orders"] == 0), 1, 0
)

# Export final Data Mart to CSV for Streamlit & ML Pipeline
dim_customers.to_csv("dim_customers_mart.csv", index=False)

print("✅ Data Mart successfully updated: 'dim_customers_mart.csv'")
print(f"Total Customers Processed: {len(dim_customers)}")
print(f"Churned Customers Rate: {dim_customers['is_churned'].mean() * 100:.1f}%")