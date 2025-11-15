import pandas as pd
import os

print("\n🚀 Preparing final Customer360 dataset...")

# Load files
master = pd.read_csv("data/processed/customer_360_master.csv")
segments = pd.read_csv("data/feature_store/customer_segments.csv")
churn = pd.read_csv("data/feature_store/churn_predictions.csv")


print(f"📥 Loaded:\n Master: {master.shape}\n Segments: {segments.shape}\n Churn: {churn.shape}")

# ---- FIX SEGMENT COLUMN NAME ----
if "segment_name" not in segments.columns:
    if "Segment_Label" in segments.columns:
        print("🔧 Renaming 'Segment_Label' → 'segment_name'")
        segments.rename(columns={"Segment_Label": "segment_name"}, inplace=True)
    elif "Segment" in segments.columns:
        print("🔧 Renaming 'Segment' → 'segment_name'")
        segments.rename(columns={"Segment": "segment_name"}, inplace=True)
    else:
        raise KeyError("❌ No segmentation column found (expected Segment_Label or Segment).")

# ---- Merge datasets ----
df = master.merge(segments[["customer_unique_id", "segment_name"]], on="customer_unique_id", how="left")
# 🧠 Merge churn values using correct column name
df = df.merge(churn[["customer_unique_id", "is_churn"]], 
              on="customer_unique_id", 
              how="left")

# Rename churn flag column for clarity
df.rename(columns={"is_churn": "churn_flag"}, inplace=True)

# Save
output_path = "data/final/customer360_final_dataset.csv"
os.makedirs("data/final", exist_ok=True)
df.to_csv(output_path, index=False)

print("\n🎉 FINAL DATASET READY!")
print(f"📁 Saved at: {output_path}")
print(f"📊 Final Shape: {df.shape}")
