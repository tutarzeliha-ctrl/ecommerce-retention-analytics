import pandas as pd
import numpy as np

# 1. Load raw datasets
users = pd.read_csv('raw_users.csv')
orders = pd.read_csv('raw_orders.csv')
order_items = pd.read_csv('raw_order_items.csv')

# 2. Filter completed orders
completed_orders = orders[orders['status'] == 'completed'].copy()
completed_orders['order_date'] = pd.to_datetime(completed_orders['order_date'])

# 3. Calculate gross revenue per line item
order_items['gross_revenue'] = (
    order_items['quantity'] * order_items['unit_price'] * (1 - order_items['discount'])
)
order_revenue = order_items.groupby('order_id')['gross_revenue'].sum().reset_index()

# 4. Merge completed orders with revenue details
orders_with_revenue = pd.merge(completed_orders, order_revenue, on='order_id', how='left')

# 5. Aggregate customer-level metrics (dbt dim_customers logic)
customer_metrics = orders_with_revenue.groupby('user_id').agg(
    total_orders=('order_id', 'nunique'),
    first_order_at=('order_date', 'min'),
    most_recent_order_at=('order_date', 'max'),
    lifetime_value_ltv=('gross_revenue', 'sum')
).reset_index()

# 6. Combine with user master records
customer_mart = pd.merge(users, customer_metrics, on='user_id', how='left')
customer_mart['total_orders'] = customer_mart['total_orders'].fillna(0)
customer_mart['lifetime_value_ltv'] = customer_mart['lifetime_value_ltv'].fillna(0)

# 7. Calculate Recency (days since most recent order)
max_date = pd.to_datetime(orders['order_date']).max()
customer_mart['recency_days'] = (
    (max_date - pd.to_datetime(customer_mart['most_recent_order_at'])).dt.days.fillna(999)
)

# 8. Define Churn Flag (Inactivity > 180 days)
customer_mart['is_churned'] = np.where(customer_mart['recency_days'] > 180, 1, 0)

# 9. Export to CSV for downstream analytics & ML (Julius AI)
customer_mart.to_csv('dim_customers_mart.csv', index=False)
print("✅ dim_customers_mart.csv has been successfully generated!")