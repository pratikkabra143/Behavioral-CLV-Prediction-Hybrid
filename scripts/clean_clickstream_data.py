import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

print("Loading clickstream data...")
df = pd.read_csv(RAW / "ecommerce_clickstream_transactions.csv")

# Basic cleanup
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df = df.dropna(subset=["UserID", "Timestamp"])
df = df.sort_values(["UserID", "Timestamp"])

# Event-type normalization
df["EventType"] = df["EventType"].str.lower().str.strip()

# Derive simple per-user metrics
user_agg = df.groupby("UserID").agg(
    total_events=("EventType", "count"),
    unique_sessions=("SessionID", "nunique"),
    page_views=("EventType", lambda x: (x == "page_view").sum()),
    add_to_cart=("EventType", lambda x: (x == "add_to_cart").sum()),
    purchases=("EventType", lambda x: (x == "purchase").sum()),
    first_event=("Timestamp", "min"),
    last_event=("Timestamp", "max"),
    avg_amount=("Amount", "mean"),
    total_amount=("Amount", "sum")
).reset_index()

# Derived behavioral features
user_agg["conversion_rate"] = (
    user_agg["purchases"] / user_agg["unique_sessions"].replace(0, 1)
).round(4)
user_agg["cart_rate"] = (
    user_agg["add_to_cart"] / user_agg["page_views"].replace(0, 1)
).round(4)
user_agg["session_activity"] = (
    user_agg["total_events"] / user_agg["unique_sessions"].replace(0, 1)
).round(2)
user_agg["engagement_days"] = (
    (user_agg["last_event"] - user_agg["first_event"]).dt.days
)

# Time-based recency
analysis_date = df["Timestamp"].max() + pd.Timedelta(days=1)
user_agg["recency_days"] = (analysis_date - user_agg["last_event"]).dt.days

# Save
out_path = PROCESSED / "clickstream_users_cleaned.csv"
user_agg.to_csv(out_path, index=False)
print(f"✅ Cleaned clickstream user data saved → {out_path}")
print(user_agg.head())
