# 🧠 Behavioral-CLV-Prediction-Hybrid

---

## 🛢️ Dataset
1. **Olist Brazilian E-Commerce Dataset**  
   [Kaggle Link](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
   - Provides order-level transactional data: orders, payments, reviews, and customers.  
   - Used to extract Recency, Frequency, and Monetary (RFM) features.

2. **E-Commerce Clickstream Transactions (Synthetic)**  
   [Kaggle Link](https://www.kaggle.com/datasets/fronkongames/ecommerce-clickstream-transactions)  
   - Simulated clickstream data: page views, cart additions, purchases, timestamps.  
   - Used for behavioral metrics like engagement, activity frequency, conversion rate, etc.

> All datasets are stored in `data/raw/`.  
> Cleaned and merged datasets are saved in `data/processed/`.

---

## 🛠 Deliverables

1. **1. Data Collection & Inventory**
   - Script: `data_inventory.py`  
   - Scans all raw `.csv` files and outputs metadata summary → `data/inventory.json`

2. **Data Preparation & Cleaning** (Transactional)
   - Script `clean_olist_data.py`
   - Cleans and aggregates transactional features.
   - Generated features include:
     - `frequency`, `total_spent`, `avg_order_value`, `recency_days`
   - Outputs saved to `data/processed/olist_customers_cleaned.csv`.

3. **Data Preparation & Cleaning** (Behavioral)
   - Script: `clean_clickstream_data.py`
   - Cleans and aggregates behavioral features.
   - Generated features include:
     - `page_views`, `add_to_cart`, `purchases`, `conversion_rate`, etc.
   - Outputs saved to `data/processed/clickstream_users_cleaned.csv`.

4. **Synthetic Mapping**
   - Script: `create_user_mapping.py`  
   - Creates a rank-based synthetic mapping between Olist customers and clickstream users for demonstration purposes.  
   - Output: `data/processed/user_mapping.csv`

---

## 📂 Project Workflow

```
Behavioral-CLV-Prediction-Hybrid/
├── data/
│   ├── processed/
│   ├── raw/                 # Original datasets (Olist + Clickstream)
│   └── inventory.json       # Data inventory summary 
│
├── outputs/
│
├── scripts/
│   ├── clean_clickstream_data.py
│   ├── clean_olist_data.py
│   ├── create_user_mapping.py
│   └── data_inventory.py
├── README.md
└── requirements.txt
```

---
