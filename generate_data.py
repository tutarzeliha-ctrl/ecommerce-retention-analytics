import numpy as np
import pandas as pd
from faker import Faker

# Set seed for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)

NUM_USERS = 1000
NUM_PRODUCTS = 50
NUM_ORDERS = 5000

# 1. USERS TABLE
user_ids = [f"USR_{1000 + i}" for i in range(NUM_USERS)]
user_channels = ["Organic", "Paid Search", "Social Media", "Referral", "Email"]
signup_dates = pd.date_range(
    start="2024-01-01", end="2025-12-31", periods=NUM_USERS
)

users_df = pd.DataFrame(
    {
        "user_id": user_ids,
        "signup_date": signup_dates,
        "country": np.random.choice(
            ["DE", "NL", "CH", "UK", "TR"],
            size=NUM_USERS,
            p=[0.3, 0.25, 0.2, 0.15, 0.1],
        ),
        "acquisition_channel": np.random.choice(
            user_channels, size=NUM_USERS, p=[0.3, 0.25, 0.2, 0.15, 0.1]
        ),
        "age": np.random.randint(18, 65, size=NUM_USERS),
    }
)

# 2. PRODUCTS TABLE
categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Sports"]
products_data = []
for i in range(1, NUM_PRODUCTS + 1):
    cat = np.random.choice(categories)
    price = round(np.random.uniform(10, 500), 2)
    cost = round(price * np.random.uniform(0.4, 0.7), 2)  # Profit margin logic
    products_data.append(
        {
            "product_id": f"PRD_{100 + i}",
            "category": cat,
            "unit_price": price,
            "unit_cost": cost,
        }
    )
products_df = pd.DataFrame(products_data)

# 3. ORDERS TABLE
order_dates = pd.date_range(
    start="2024-02-01", end="2026-06-30", periods=NUM_ORDERS
)
orders_df = pd.DataFrame(
    {
        "order_id": [f"ORD_{10000 + i}" for i in range(NUM_ORDERS)],
        "user_id": np.random.choice(user_ids, size=NUM_ORDERS),
        "order_date": order_dates,
        "status": np.random.choice(
            ["completed", "returned", "cancelled"],
            size=NUM_ORDERS,
            p=[0.82, 0.12, 0.06],
        ),
    }
)

# 4. ORDER_ITEMS TABLE
order_items_data = []
item_id_counter = 1
for order_id in orders_df["order_id"]:
    num_items = np.random.randint(1, 4)  # 1 to 3 items per basket
    for _ in range(num_items):
        product = products_df.sample(1).iloc[0]
        qty = np.random.randint(1, 3)
        discount = np.random.choice([0.0, 0.05, 0.10, 0.20], p=[0.6, 0.2, 0.1, 0.1])
        order_items_data.append(
            {
                "item_id": f"ITM_{item_id_counter}",
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": qty,
                "unit_price": product["unit_price"],
                "discount": discount,
            }
        )
        item_id_counter += 1

order_items_df = pd.DataFrame(order_items_data)

# Save to CSV files
users_df.to_csv("raw_users.csv", index=False)
products_df.to_csv("raw_products.csv", index=False)
orders_df.to_csv("raw_orders.csv", index=False)
order_items_df.to_csv("raw_order_items.csv", index=False)

print("✅ 4 Raw Datasets Successfully Generated in English!")