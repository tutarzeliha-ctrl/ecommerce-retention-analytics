Markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ecommerce-retention-analytics-2eyfdwkwncg2h4tmrpnzfp.streamlit.app/)

# 🛒 E-Commerce Customer Retention, LTV & ML Churn Analytics Pipeline

An end-to-end modern data stack (MDS) implementation and machine learning analytics pipeline designed to analyze customer retention, Lifetime Value (LTV), and churn risk for European e-commerce platforms.

---

## 🏗 Architecture Overview

```text
[ Raw Data Sources (CSV) ]
           │
           ▼
[ dbt Transformation Pipeline ]
   ├── Staging Layer (`stg_users`, `stg_orders`, `stg_order_items`)
   └── Analytics Mart (`dim_customers_mart`)
           │
           ▼
[ Machine Learning & Analytics Layer (Julius AI) ]
   ├── RFM Customer Segmentation
   └── Random Forest Churn Prediction Model (ROC-AUC: 0.8687)
📊 Analytics & Machine Learning Insights
1. Customer RFM Segmentation
Active customers are segmented based on Recency, Frequency, and Monetary (RFM) metrics:

Champions: Average LTV of ~$5,567 (Highest revenue drivers)

Loyal Customers: Average LTV of ~$4,572

At Risk: Average LTV of ~$3,673

Lost Customers: Average LTV of ~$1,950

2. Machine Learning Churn Prediction
A Random Forest Classifier was trained on customer behavior features to predict potential churn (is_churned defined as >180 days of inactivity).

Model Performance (ROC-AUC Score): 0.8687

Primary Churn Drivers:

Lifetime Value (LTV): Lower monetary contribution strongly correlates with churn risk.

Age: Demographics impact long-term engagement.

Total Orders: Order frequency serves as a key retention indicator.

🛠 Tech Stack & Standards
Data Transformation & Modeling: SQL, dbt (Data Build Tool)

Data Engineering & Scripting: Python (Pandas, NumPy)

Machine Learning & Visualization: Scikit-Learn, Seaborn, Julius AI

Version Control: Git, GitHub

## 🚀 How to Run Locally

### 1. Activate Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
python generate_data.py
python export_mart_data.py
python eda_analysis.py
```