Markdown

# 🛒 E-Commerce Retention & Churn Analytics

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ecommerce-retention-analytics.streamlit.app/)

> 📹 **Watch 2-Min Architecture & Demo Video:**  
> [▶️ Watch Demo on YouTube](https://youtu.be/Rz-U4KjB0ys)

---

## 🚀 How to Run the Pipeline

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tutarzeliha-ctrl/ecommerce-retention-analytics.git](https://github.com/tutarzeliha-ctrl/ecommerce-retention-analytics.git)
   cd ecommerce-retention-analytics
   
# 🛒 E-Commerce Retention & Churn Analytics Pipeline

An end-to-end modern data engineering solution designed to model raw e-commerce data, evaluate retention metrics, and trigger automated Reverse ETL churn alerts.

---

## ## 🏗️ Architecture & Data Flow

```text
[Raw CSV / Synthetic Data] 
            │
            ▼
   [Google BigQuery] ──► [dbt Core (Staging & Marts)] ──► [dbt Tests (6/6 PASS)]
                                      │
                                      ▼
                        [Reverse ETL / Webhook Alerts]


---

  **💡 Business Impact & Core Value**  
> This project provides an actionable, end-to-end data product that not only uncovers data insights but also facilitates direct business action to minimize customer attrition.
For example, by identifying high-churn-risk users and automating alert systems, the marketing team can proactively re-engage these customers, potentially saving the business significant revenue.



## 🚀 Key Project Features

* **Data Transformations:** Built modular `staging` and `marts` models using **dbt Core** and **Google BigQuery**.
* **Data Quality & Observability:** Implemented primary key tests (`unique`, `not_null`) across core models achieving **100% test pass rate**.
* **Reverse ETL Automation:** Automated Python pipeline identifying high-churn-risk users and formatting webhook payloads for CRM/Slack notifications.
* **Exploratory Data Analysis (EDA):** Evaluated performance metrics (€3.2M+ Revenue, €796 AOV, 82.2% completion rate).

---

## 🛠️ Tech Stack

* **Data Warehouse:** Google BigQuery
* **Data Transformation:** dbt Core (`dbt-bigquery`)
* **Language & Automation:** Python, Pandas
* **CI/CD:** GitHub Actions
