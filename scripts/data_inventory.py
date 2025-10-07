import os, json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")
OUT_FILE = Path("data/inventory.json")
OUT = {}

def count_rows_quick(file_path):
    with open(file_path, 'rb') as f:
        return sum(1 for _ in f) - 1  # minus header line

for file in sorted(DATA_DIR.glob("*.csv")):
    info = {
        "path": str(file),
        "size_kb": round(file.stat().st_size / 1024, 2)
    }
    try:
        sample = pd.read_csv(file, nrows=5)
        info["columns"] = list(sample.columns)
        info["first_row"] = sample.iloc[0].to_dict()
        info["dtypes"] = {c: str(sample[c].dtype) for c in sample.columns}
        info["approx_rows"] = count_rows_quick(file)
        likely_dates = []
        for c in sample.columns:
            try:
                parsed = pd.to_datetime(sample[c], errors='coerce')
                if parsed.notna().sum() > 0:
                    likely_dates.append(c)
            except Exception:
                pass
        info["likely_date_columns"] = likely_dates
    except Exception as e:
        info["error"] = str(e)
    OUT[file.name] = info

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=2)
print(f"Inventory saved → {OUT_FILE}")