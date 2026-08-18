# 🛒 E-Commerce Customer Retention & LTV Analytics Pipeline

An end-to-end modern data stack (MDS) implementation designed to analyze customer retention, Lifetime Value (LTV), and churn risk for European e-commerce platforms.

---

## 📐 Architecture Overview

```text
[ Raw CSV / Data Source ]
         │
         ▼
[ Python EDA & Analytics ] ──> Exploratory Data Analysis & Business Metrics
         │
         ▼
[ dbt Data Pipeline ]
   ├── Staging Layer (`stg_users`, `stg_orders`, `stg_order_items`)
   └── Marts Layer (`dim_customers` - LTV & Churn Modeling)

🎯 Key Business Questions Addressed
Customer Lifetime Value (LTV): How much revenue does each customer segment generate over time?

Churn Risk Detection: Identifying customers who haven't ordered in the last 180 days.

Regional Revenue Contribution: Analysis across core European markets (Germany, Netherlands, Switzerland, UK, Turkey).

📊 Business Key Performance Indicators (KPIs)
Order Status: ~82.2% Completed | ~12.1% Returned | ~5.7% Cancelled

Top Revenue Markets:

Germany (DE): ~$1.05M

Netherlands (NL): ~$772K

Switzerland (CH): ~$647K

Primary Acquisition Channels: Organic Search & Paid Search drive highest LTV.

🛠️ Tech Stack & Tools
SQL / dbt: Data transformation, dimensional modeling, and business logic materialization.

Python (Pandas, Numpy, Faker): Synthetic transactional data generation and exploratory analysis.

Modern Data Stack Standards: Modular SQL layering (Staging -> Marts).

🚀 How to Run Locally
Activate Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
Generate Raw Datasets:

Bash
python generate_data.py
Run Exploratory Data Analysis:

Bash
python eda_analysis.py