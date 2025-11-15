import pandas as pd

RAW_PATH = "data/raw/olist_orders_dataset.csv"

def load_data():
    print("🔹 Loading orders dataset...")
    df = pd.read_csv(RAW_PATH)
    print("Shape:", df.shape)
    return df

def clean_data(df):
    print("\n🔹 Cleaning orders dataset...")

    # Remove rows with missing order_id
    df = df.dropna(subset=["order_id"])

    # Convert timestamps to datetime
    date_cols = [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Standardize column names
    df = df.rename(columns={
        "customer_id": "customer_id",
        "order_status": "status",
    })

    # Remove corrupted rows with invalid dates
    df = df[df["order_purchase_timestamp"].notnull()]

    return df

def save_data(df):
    output_path = "data/cleaned/orders_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved cleaned dataset to: {output_path}")

if __name__ == "__main__":
    df = load_data()
    print(df.head())
    print(df.info())
    print(df.isnull().sum())

    df = clean_data(df)
    save_data(df)
