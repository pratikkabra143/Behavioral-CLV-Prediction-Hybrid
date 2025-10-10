import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

print("Loading processed datasets...")
olist = pd.read_csv(PROCESSED / "olist_customers_cleaned.csv")
clicks = pd.read_csv(PROCESSED / "clickstream_users_cleaned.csv")
mapping = pd.read_csv(PROCESSED / "user_mapping.csv")

# Merge transactional + behavioral
merged = (
    mapping
    .merge(olist, on="customer_unique_id", how="left")
    .merge(clicks, on="UserID", how="left")
)

print("✅ Datasets merged successfully!")
print("Rows:", len(merged))

# Fill numeric NaNs with 0
num_cols = merged.select_dtypes(include=["float64", "int64"]).columns
merged[num_cols] = merged[num_cols].fillna(0)

# Derived hybrid ratios
merged["engagement_value_ratio"] = (
    merged["total_spent"] / merged["total_events"].replace(0, 1)
).round(3)
merged["activity_frequency_ratio"] = (
    merged["frequency"] / merged["unique_sessions"].replace(0, 1)
).round(3)

# Save output
out_path = PROCESSED / "hybrid_features.csv"
merged.to_csv(out_path, index=False)
print(f"✅ Hybrid dataset saved → {out_path}")
print(merged.head())
