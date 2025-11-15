import pandas as pd

RAW_PATH = "data/raw/olist_sellers_dataset.csv"

def load_data():
    print("🔹 Loading sellers dataset...")
    df = pd.read_csv(RAW_PATH)
    print("Shape:", df.shape)
    return df

def clean_data(df):
    print("\n🔹 Cleaning sellers dataset...")

    # Remove duplicate sellers
    df = df.drop_duplicates(subset=["seller_id"])

    # Rename columns for consistency
    df = df.rename(columns={
        "seller_zip_code_prefix": "zip_prefix",
        "seller_city": "city",
        "seller_state": "state"
    })

    return df

def save_data(df):
    output_path = "data/cleaned/sellers_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved cleaned dataset to: {output_path}")

if __name__ == "__main__":
    df = load_data()
    print(df.head())
    print(df.info())
    print(df.isnull().sum())

    df = clean_data(df)
    save_data(df)
