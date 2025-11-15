import pandas as pd
import os

CLEANED_DIR = "data/cleaned"
OUTPUT_PATH = "data/processed/customer_360_master.csv"


def load_dataset(filename):
    path = os.path.join(CLEANED_DIR, filename)
    print(f"📥 Loading {filename} ...")
    df = pd.read_csv(path)
    print(f"   👉 Columns: {list(df.columns)}\n")
    return df


def main():
    print("\n🔹 Starting dataset integration...")

    # Load datasets
    customers = load_dataset("customers_cleaned.csv")
    orders = load_dataset("orders_cleaned.csv")
    items = load_dataset("order_items_cleaned.csv")
    sellers = load_dataset("sellers_cleaned.csv")
    marketing = load_dataset("marketing_campaign_cleaned.csv")

    # 🔧 Fix key column names
    print("🔧 Standardizing key column names...")

    if "unique_id" in customers.columns:
        customers.rename(columns={"unique_id": "customer_unique_id"}, inplace=True)

    if "ID" in marketing.columns:
        marketing.rename(columns={"ID": "customer_unique_id"}, inplace=True)

    print(f"   👉 Customers Columns: {list(customers.columns)}")
    print(f"   👉 Marketing Columns: {list(marketing.columns)}\n")

    # Ensure matching datatypes for merging
    customers["customer_unique_id"] = customers["customer_unique_id"].astype(str)
    marketing["customer_unique_id"] = marketing["customer_unique_id"].astype(str)

    # 🔁 Start merging process
    print("🔹 Merging orders with order items...")
    merged = pd.merge(orders, items, on="order_id", how="left")

    print("🔹 Merging customers...")
    merged = pd.merge(merged, customers, on="customer_id", how="left")

    print("🔹 Merging sellers info...")
    merged = pd.merge(merged, sellers, on="seller_id", how="left")

    print("🔹 Merging marketing campaign data...")
    merged = pd.merge(merged, marketing, on="customer_unique_id", how="left")

    # 🔍 Final summary
    print("\n📊 Final dataset shape:", merged.shape)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)

    print(f"\n✅ Customer 360 Master dataset saved to:\n   {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
