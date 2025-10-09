import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

print("Loading cleaned data...")
olist = pd.read_csv(PROCESSED / "olist_customers_cleaned.csv")
clicks = pd.read_csv(PROCESSED / "clickstream_users_cleaned.csv")

# Select key ranking metrics
olist["activity_score"] = (
    olist["frequency"].rank(method="first", ascending=False) +
    olist["total_spent"].rank(method="first", ascending=False)
)
clicks["activity_score"] = (
    clicks["total_events"].rank(method="first", ascending=False) +
    clicks["total_amount"].rank(method="first", ascending=False)
)

# Sort both datasets by activity
olist_sorted = olist.sort_values("activity_score", ascending=False).reset_index(drop=True)
clicks_sorted = clicks.sort_values("activity_score", ascending=False).reset_index(drop=True)

# Equalize lengths
min_len = min(len(olist_sorted), len(clicks_sorted))
olist_sorted = olist_sorted.head(min_len)
clicks_sorted = clicks_sorted.head(min_len)

# Create 1:1 mapping
mapping = pd.DataFrame({
    "customer_unique_id": olist_sorted["customer_unique_id"].values,
    "UserID": clicks_sorted["UserID"].values
})

# Save mapping
out_path = PROCESSED / "user_mapping.csv"
mapping.to_csv(out_path, index=False)
print(f"✅ Synthetic mapping created → {out_path}")
print(mapping.head())
