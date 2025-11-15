import pandas as pd
import os

RAW_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "marketing_campaign.csv")
CLEAN_PATH = "../data/cleaned/marketing_campaign_cleaned.csv"

def load_data():
    print("🔹 Loading dataset...")
    df = pd.read_csv(RAW_PATH, sep=None, engine="python")
    print("Dataset Loaded: ", df.shape)
    return df


def clean_data(df):
    print("\n🔹 Cleaning dataset...")

    # Convert Dt_Customer to datetime
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], format="%d-%m-%Y")

    # Fill missing Income
    df["Income"] = df["Income"].fillna(df["Income"].median())

    # Feature engineering
    df["Customer_Age"] = 2025 - df["Year_Birth"]

    mnt_cols = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts",
                "MntSweetProducts", "MntGoldProds"]
    df["Total_Spent"] = df[mnt_cols].sum(axis=1)

    purchase_cols = ["NumDealsPurchases", "NumWebPurchases",
                     "NumCatalogPurchases", "NumStorePurchases"]
    df["Total_Purchases"] = df[purchase_cols].sum(axis=1)

    df["Family_Size"] = df["Kidhome"] + df["Teenhome"] + 2

    df["Days_Since_Enrolled"] = (
        pd.Timestamp("2025-01-01") - df["Dt_Customer"]
    ).dt.days

    return df


def save_data(df):
    output_path = "data/cleaned/marketing_campaign_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved cleaned dataset to: {output_path}")


if __name__ == "__main__":
    df = load_data()
    print("\n🔹 First 5 rows:")
    print(df.head())

    print("\n🔹 Info:")
    print(df.info())

    print("\n🔹 Missing values:")
    print(df.isnull().sum())

    df = clean_data(df)
    save_data(df)
