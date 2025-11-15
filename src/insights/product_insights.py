import os
import pandas as pd

print("\n📥 Searching for dataset...")

EXPECTED_FILE = "customer360_final_dataset.csv"
DATA_PATH = None

# Search for file in project
for root, dirs, files in os.walk("."):
    if EXPECTED_FILE in files:
        DATA_PATH = os.path.join(root, EXPECTED_FILE)
        break

if DATA_PATH is None:
    print(f"❌ ERROR: '{EXPECTED_FILE}' not found anywhere in the project!")
    print("👉 Make sure it exists before running insights.")
    exit()

print(f"✔ Found dataset at: {DATA_PATH}")

# Load dataset
df = pd.read_csv(DATA_PATH)
print("\n📥 Dataset Loaded Successfully!\n")

# ---- Determine the correct grouping column ----
possible_columns = ["product_category_name", "product_name", "product_id"]

group_column = next((col for col in possible_columns if col in df.columns), None)

if not group_column:
    print("\n❌ ERROR: No product attribute column found!")
    print("👉 Expected one of: product_category_name, product_name, or product_id")
    exit()

if group_column != "product_category_name":
    print(f"⚠️ Using '{group_column}' because 'product_category_name' is missing.\n")
else:
    print("✔ Using 'product_category_name' for insights.\n")

# ---- Create spending column ----
if "Total_Spent" in df.columns:
    df["total_spend"] = df["Total_Spent"]
    print("✔ Using existing 'Total_Spent' column.\n")
elif "price" in df.columns:
    print("⚠️ 'Total_Spent' missing — computing spend using 'price' column...\n")
    df["total_spend"] = df["price"]
else:
    print("❌ ERROR: Cannot compute spend: No 'price' or 'Total_Spent' column available.")
    exit()

# ---- Aggregate spend ----
print("📊 Calculating total spend by product attribute...\n")

spend_stats = df.groupby(group_column)["total_spend"].sum().reset_index()
spend_stats = spend_stats.sort_values(by="total_spend", ascending=False)

print("🏆 Top 10 Products by Spend:\n")
print(spend_stats.head(10))

# ---- Save output ----
os.makedirs("outputs", exist_ok=True)
output_path = "outputs/product_spend_insights.csv"
spend_stats.to_csv(output_path, index=False)

print(f"\n💾 Insights saved to: {output_path}")
print("✅ Completed!\n")
