import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load raw datasets
users_df = pd.read_csv("raw_users.csv")
products_df = pd.read_csv("raw_products.csv")
orders_df = pd.read_csv("raw_orders.csv")
order_items_df = pd.read_csv("raw_order_items.csv")

# 1. Calculate Key Performance Indicators (KPIs)
# Merge orders with items to get total revenue
merged_orders = order_items_df.merge(orders_df, on="order_id")
merged_orders["item_total"] = merged_orders["quantity"] * merged_orders[
    "unit_price"
] * (1 - merged_orders["discount"])

completed_orders = merged_orders[merged_orders["status"] == "completed"]

total_revenue = round(completed_orders["item_total"].sum(), 2)
total_completed_orders_count = orders_df[orders_df["status"] == "completed"][
    "order_id"
].nunique()
aov = round(total_revenue / total_completed_orders_count, 2)

print("\n==========================================")
print("📊 KEY PERFORMANCE INDICATORS (KPIs)")
print("==========================================")
print(f"Total Revenue (Completed Orders): €{total_revenue:,.2f}")
print(f"Average Order Value (AOV): €{aov:,.2f}")
print(f"Total Completed Orders: {total_completed_orders_count}")

# Order Status Breakdown
status_dist = orders_df["status"].value_counts(normalize=True) * 100
print("\nOrder Status Distribution (%):")
for status, pct in status_dist.items():
    print(f"  - {status.capitalize()}: {pct:.1f}%")

# 2. Customer Demographics
print("\n==========================================")
print("🌍 USER DEMOGRAPHICS SUMMARY")
print("==========================================")
country_dist = users_df["country"].value_counts()
print("Users by Country:")
for country, count in country_dist.items():
    print(f"  - {country}: {count} users")

# 3. Generate Visualizations
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: User Distribution by Country
sns.barplot(
    x=country_dist.index,
    y=country_dist.values,
    ax=axes[0],
    palette="viridis",
    hue=country_dist.index,
    legend=False,
)
axes[0].set_title("User Distribution by Target Country", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Country Code")
axes[0].set_ylabel("Number of Users")

# Plot 2: Revenue by Category
category_revenue = completed_orders.merge(products_df, on="product_id").groupby("category")["item_total"].sum().reset_index()
sns.barplot(
    data=category_revenue,
    x="item_total",
    y="category",
    ax=axes[1],
    palette="mako",
    hue="category",
    legend=False,
)
axes[1].set_title("Total Revenue by Product Category (€)", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Total Revenue (€)")
axes[1].set_ylabel("Category")

plt.tight_layout()
plt.savefig("assets/eda_summary_charts.png")
print("\n✅ EDA Completed! Visualizations saved to 'assets/eda_summary_charts.png'.")