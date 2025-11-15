import pandas as pd
import os

RAW_FILE = "data/raw/olist_order_items_dataset.csv"
OUTPUT_FILE = "data/cleaned/order_items_cleaned.csv"

def main():
    print("\n🔹 Loading order_items dataset...")
    df = pd.read_csv(RAW_FILE)

    print("\n📌 Original columns:", list(df.columns))

    # Rename for consistency
    df.rename(columns={
        "order_id": "order_id",
        "order_item_id": "item_no",
        "product_id": "product_id",
        "seller_id": "seller_id",
        "shipping_limit_date": "shipping_limit_date",
        "price": "price",
        "freight_value": "freight_cost"
    }, inplace=True)

    # Convert date formats
    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")

    # Fill missing values if any
    df.fillna({"freight_cost": 0, "price": 0}, inplace=True)

    print("\n📌 Cleaned columns:", list(df.columns))
    print(f"\n📊 Shape: {df.shape}")

    # Save cleaned file
    os.makedirs("data/cleaned", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Saved cleaned order_items dataset → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
