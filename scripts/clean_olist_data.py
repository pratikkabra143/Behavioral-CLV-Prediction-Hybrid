import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

print("Loading Olist CSVs...")
orders = pd.read_csv(RAW / "olist_orders_dataset.csv", parse_dates=[
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
])
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
payments = pd.read_csv(RAW / "olist_order_payments_dataset.csv")
customers = pd.read_csv(RAW / "olist_customers_dataset.csv")

# Merge transactional data
# Revenue per order
order_items_agg = (
    items.groupby("order_id")
    .agg({"price": "sum", "freight_value": "sum"})
    .reset_index()
    .rename(columns={"price": "total_price", "freight_value": "total_freight"})
)

# Merge all relevant info
merged = (
    orders
    .merge(order_items_agg, on="order_id", how="left")
    .merge(payments.groupby("order_id").agg({"payment_value": "sum"}).reset_index(),
           on="order_id", how="left")
    .merge(customers, on="customer_id", how="left")
)

# Basic cleaning
merged = merged[merged["order_status"] == "delivered"]        # keep delivered orders
merged.dropna(subset=["order_purchase_timestamp"], inplace=True)
merged["order_purchase_timestamp"] = pd.to_datetime(merged["order_purchase_timestamp"])
analysis_date = merged["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

# Aggregate to customer level
cust_agg = (
    merged.groupby("customer_unique_id")
    .agg(
        first_purchase=("order_purchase_timestamp", "min"),
        last_purchase=("order_purchase_timestamp", "max"),
        frequency=("order_id", "nunique"),
        total_spent=("payment_value", "sum"),
        avg_order_value=("payment_value", "mean")
    )
    .reset_index()
)
cust_agg["recency_days"] = (analysis_date - cust_agg["last_purchase"]).dt.days

# Save
out_path = PROCESSED / "olist_customers_cleaned.csv"
cust_agg.to_csv(out_path, index=False)
print(f"✅ Cleaned Olist customer data saved → {out_path}")
print(cust_agg.head())
