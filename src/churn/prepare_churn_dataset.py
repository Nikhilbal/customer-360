import pandas as pd
import os

# Input / output
MASTER_PATH = "data/processed/customer_360_master.csv"
OUT_DIR = "data/feature_store"
OUT_PATH = os.path.join(OUT_DIR, "churn_dataset.csv")

def load_master():
    print(f"📥 Loading master dataset from {MASTER_PATH} ...")
    return pd.read_csv(MASTER_PATH, low_memory=False)

def prepare_churn_dataset(df, churn_days=180):
    print("🔧 Preparing churn dataset and features...")

    # Ensure datetime
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')

    # Snapshot date = latest purchase date in dataset
    snapshot = df['order_purchase_timestamp'].max()
    print(f"   Snapshot date (latest purchase): {snapshot}")

    # Aggregate per customer
    agg = df.groupby('customer_unique_id').agg(
        last_purchase_date=('order_purchase_timestamp', 'max'),
        first_purchase_date=('order_purchase_timestamp', 'min'),
        frequency=('order_id', 'nunique'),
        monetary=('price', 'sum')
    ).reset_index()

    # Derived features
    agg['recency_days'] = (snapshot - agg['last_purchase_date']).dt.days
    agg['customer_age_days'] = (agg['last_purchase_date'] - agg['first_purchase_date']).dt.days.fillna(0)
    agg['avg_order_value'] = agg['monetary'] / agg['frequency'].replace({0:1})

    # Churn label: 1 = churned (no purchase within churn_days), 0 = active
    agg['is_churn'] = (agg['recency_days'] > churn_days).astype(int)

    # Keep useful columns
    result = agg[[
        'customer_unique_id', 'last_purchase_date', 'first_purchase_date',
        'recency_days', 'frequency', 'monetary', 'avg_order_value',
        'customer_age_days', 'is_churn'
    ]].copy()

    # Fill / tidy
    result.fillna({'monetary': 0, 'avg_order_value': 0}, inplace=True)

    return result

def save_features(df):
    os.makedirs(OUT_DIR, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"✅ Churn dataset saved to: {OUT_PATH}")

def main():
    df = load_master()
    churn_df = prepare_churn_dataset(df, churn_days=180)
    save_features(churn_df)
    print("\n🎯 Churn dataset preparation complete.")

if __name__ == "__main__":
    main()
