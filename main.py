import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

# 1. Load Data Mart
df = pd.read_csv("dim_customers_mart.csv")

# ---------------------------------------------------------
# 2. RFM SEGMENTATION
# ---------------------------------------------------------
active_df = df[df["is_churned"] == 0].copy()

# Recency, Frequency, Monetary Score Calculation (1 to 4)
active_df["R_Score"] = pd.qcut(
    active_df["recency_days"], q=4, labels=[4, 3, 2, 1]
)
active_df["F_Score"] = pd.qcut(
    active_df["total_orders"].rank(method="first"),
    q=4,
    labels=[1, 2, 3, 4],
)
active_df["M_Score"] = pd.qcut(
    active_df["lifetime_value_ltv"].rank(method="first"),
    q=4,
    labels=[1, 2, 3, 4],
)

active_df["RFM_Score"] = (
    active_df["R_Score"].astype(str)
    + active_df["F_Score"].astype(str)
    + active_df["M_Score"].astype(str)
)


def segment_rfm(row):
    r, f, m = int(row["R_Score"]), int(row["F_Score"]), int(row["M_Score"])
    if r >= 3 and f >= 3 and m >= 3:
        return "Champions"
    elif r >= 3 and (f >= 2 or m >= 2):
        return "Loyal Customers"
    elif r <= 2 and f >= 2:
        return "At Risk"
    else:
        return "Lost"


active_df["rfm_segment"] = active_df.apply(segment_rfm, axis=1)

print("\n==========================================")
print("📊 RFM SEGMENTATION SUMMARY")
print("==========================================")
print(active_df["rfm_segment"].value_counts())

# Save RFM Visualization
plt.figure(figsize=(8, 5))
sns.barplot(
    x=active_df["rfm_segment"].value_counts().index,
    y=active_df["rfm_segment"].value_counts().values,
    palette="viridis",
)
plt.title("Customer Distribution by RFM Segment", fontsize=12, fontweight="bold")
plt.xlabel("RFM Segment")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig("assets/rfm_segmentation.png")

# ---------------------------------------------------------
# 3. MACHINE LEARNING CHURN PREDICTION
# ---------------------------------------------------------
# Feature Engineering / One-Hot Encoding
features = ["age", "country", "acquisition_channel", "total_orders", "lifetime_value_ltv"]
X = pd.get_dummies(df[features], drop_first=True)
y = df["is_churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

auc_score = roc_auc_score(y_test, y_proba)

print("\n==========================================")
print("🤖 MACHINE LEARNING CHURN MODEL RESULTS")
print("==========================================")
print(f"ROC-AUC Score: {auc_score:.4f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save Feature Importance Plot
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=True)
plt.figure(figsize=(8, 5))
importances.tail(10).plot(kind="barh", color="#2b5c8f")
plt.title("Top Feature Importances for Churn Prediction", fontsize=12, fontweight="bold")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig("assets/churn_feature_importance.png")

print("\n✅ RFM Analysis and Churn Model finished! Charts saved in 'assets/' directory.")