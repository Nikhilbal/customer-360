import pandas as pd

RAW_PATH = "data/raw/olist_customers_dataset.csv"

def load_data():
    print("🔹 Loading customers dataset...")
    df = pd.read_csv(RAW_PATH)
    print("Shape:", df.shape)
    return df


def clean_data(df):
    print("\n🔹 Cleaning customers dataset...")

    # Drop duplicates
    df = df.drop_duplicates(subset=["customer_id"])

    # Rename columns for readability
    df = df.rename(columns={
        "customer_unique_id": "unique_id",
        "customer_zip_code_prefix": "zip_prefix",
        "customer_city": "city",
        "customer_state": "state"
    })

    return df


def save_data(df):
    output_path = "data/cleaned/customers_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved cleaned dataset to: {output_path}")


if __name__ == "__main__":
    df = load_data()
    print(df.head())
    print(df.info())
    print(df.isnull().sum())

    df = clean_data(df)
    save_data(df)
