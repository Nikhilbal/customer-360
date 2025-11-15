import pandas as pd
import os

OUTPUT_DIR = "data/insights/segmentation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📥 Loading final Customer360 dataset...")
df = pd.read_csv("data/final/customer360_final_dataset.csv")

print("🔧 Cleaning column names...")
df.columns = df.columns.str.lower().str.strip()

# ============= 1. SEGMENT SIZE =============
print("📊 Calculating segment sizes...")
segment_sizes = df["segment_name"].value_counts().reset_index()
segment_sizes.columns = ["segment_name", "customer_count"]
segment_sizes.to_csv(f"{OUTPUT_DIR}/segment_sizes.csv", index=False)

# ============= 2. AVG SPEND PER SEGMENT =============
print("💰 Calculating avg spend per segment...")
avg_spend = df.groupby("segment_name")["total_spend"].mean().reset_index()
avg_spend.columns = ["segment_name", "avg_total_spend"]
avg_spend.to_csv(f"{OUTPUT_DIR}/avg_spend_by_segment.csv", index=False)

# ============= 3. AVG CLV PER SEGMENT =============
if "clv" in df.columns:
    print("📈 Calculating CLV per segment...")
    clv_seg = df.groupby("segment_name")["clv"].mean().reset_index()
    clv_seg.columns = ["segment_name", "avg_clv"]
    clv_seg.to_csv(f"{OUTPUT_DIR}/clv_by_segment.csv", index=False)
else:
    print("⚠️ CLV column not found. Skipping CLV calculations.")

# ============= 4. CHURN % PER SEGMENT =============
print("📉 Calculating churn rate per segment...")
churn_seg = df.groupby("segment_name")["churn"].mean().reset_index()
churn_seg.columns = ["segment_name", "churn_rate"]
churn_seg.to_csv(f"{OUTPUT_DIR}/churn_rate_by_segment.csv", index=False)

# ============= 5. SEGMENT BEHAVIOR FEATURES =============
print("🔍 Generating segment behavior summary...")
behavior_cols = [
    "avg_days_between_purchases",
    "avg_order_value",
    "total_orders",
    "total_spend"
]

behavior = df.groupby("segment_name")[behavior_cols].mean().reset_index()
behavior.to_csv(f"{OUTPUT_DIR}/segment_behavior.csv", index=False)

print("\n🎉 Segmentation Insights Complete!")
print(f"📁 Saved to: {OUTPUT_DIR}")
