import pandas as pd
import os

INPUT_FILE = "data/processed/customer_360_master.csv"
OUTPUT_FILE = "data/feature_store/customer360_features.csv"

def load_master_data():
    print(f"📥 Loading master dataset from {INPUT_FILE} ...")
    return pd.read_csv(INPUT_FILE)

def engineer_features(df):
    print("\n🔧 Generating segmentation features...")

    # Fix timestamp format
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")

    # Use the most recent date for Recency calculation
    snapshot_date = df["order_purchase_timestamp"].max()

    # Ensure price column exists — if not, use freight_cost
    monetary_column = "price" if "price" in df.columns else "freight_cost"

    print(f"📌 Monetary value source column: {monetary_column}")

    # RFM feature creation
    rfm = df.groupby("customer_unique_id").agg(
        Recency=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
        Frequency=("order_id", "nunique"),
        Monetary=(monetary_column, "sum")
    ).reset_index()

    # Additional features
    rfm["CLV"] = rfm["Monetary"] * rfm["Frequency"]
    rfm["Avg_Order_Value"] = rfm["Monetary"] / rfm["Frequency"]

    print("✅ Feature engineering complete.")
    return rfm

    print("\n🔧 Generating segmentation features...")

    # RFM Features
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
    snapshot_date = df["order_purchase_timestamp"].max()

    rfm = df.groupby("customer_unique_id").agg(
        Recency=lambda x: (snapshot_date - x.max()).days,
        Frequency=("order_id", "nunique"),
        Monetary=("price", "sum")
    ).reset_index()

    # Customer Lifetime Value (simplified version)
    rfm["CLV"] = rfm["Monetary"] * rfm["Frequency"]

    # Average Order Value
    rfm["Avg_Order_Value"] = rfm["Monetary"] / rfm["Frequency"]

    print("✅ Feature engineering complete.")
    return rfm

def save_features(df):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n📁 Features successfully saved to:\n   {OUTPUT_FILE}")

def main():
    print("\n🚀 Starting feature engineering for segmentation...\n")
    
    df = load_master_data()
    features = engineer_features(df)
    save_features(features)

    print("\n🎯 All done — segmentation dataset ready!")

if __name__ == "__main__":
    main()
