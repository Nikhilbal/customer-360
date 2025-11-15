import pandas as pd
import joblib
import os

print("\n📥 Loading final dataset...")
df = pd.read_csv("data/final/customer360_final_dataset.csv")

print("📥 Loading churn model...")
model = joblib.load("models/churn_model.pkl")

print("\n🔧 Preparing features for prediction...")

# Required model input features (5 expected)
feature_map = {
    "recency_days": "Recency",
    "frequency": "Total_Purchases",
    "monetary": "Total_Spent",
    "avg_order_value": "avg_order_value",  # compute if missing
    "customer_age_days": "Days_Since_Enrolled"
}

# Compute avg_order_value if missing
if "avg_order_value" not in df.columns:
    print("⚠️ 'avg_order_value' missing — computing it...")
    df["avg_order_value"] = df["Total_Spent"] / df["Total_Purchases"]
    df["avg_order_value"] = df["avg_order_value"].fillna(0)

# Build final model-ready feature list
feature_columns = [
    feature_map["recency_days"],
    feature_map["frequency"],
    feature_map["monetary"],
    "avg_order_value",
    feature_map["customer_age_days"]
]

print("👉 Using model features:", feature_columns)

print("\n🔍 Running churn predictions...")
df["predicted_churn_probability"] = model.predict_proba(df[feature_columns])[:, 1]
df["predicted_churn_flag"] = (df["predicted_churn_probability"] > 0.5).astype(int)

print("\n📊 Top 10 highest churn risk customers:")
print(df[["customer_unique_id", "predicted_churn_probability"]]
      .sort_values(by="predicted_churn_probability", ascending=False)
      .head(10))

# Save output
os.makedirs("data/insights", exist_ok=True)
output_path = "data/insights/churn_predictions.csv"
df.to_csv(output_path, index=False)

print(f"\n💾 Churn predictions saved → {output_path}")
print("✅ Completed!")
