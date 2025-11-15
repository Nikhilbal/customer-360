import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("\n📥 Loading Customer360 final dataset...")

FILE = "data/final/customer360_final_dataset.csv"

try:
    df = pd.read_csv(FILE)
    print(f"✔ Loaded dataset: {FILE}")
except FileNotFoundError:
    print("❌ ERROR: Customer360 dataset not found.")
    exit()

print("\n📊 Dataset overview:")
print(df.head())

print("\n📏 Summary statistics:")
print(df.describe())

# Missing values check
print("\n🔍 Missing Values Count:")
print(df.isnull().sum())

# Simple Visualization
print("\n📈 Plotting segmentation distribution (if exists)...")
if "segment_name" in df.columns:
    sns.countplot(x=df["segment_name"])
    plt.title("Customer Segment Distribution")
    plt.xticks(rotation=45)
    plt.show()
else:
    print("⚠ No 'segment_name' column found, skipping segment plot.")
