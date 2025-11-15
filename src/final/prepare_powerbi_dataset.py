import pandas as pd

print("\n🚀 STEP 0 – Preparing dataset for Power BI...\n")

# Load the final dataset created earlier
df = pd.read_csv("data/final/customer360_final_dataset.csv")

print(f"📥 Loaded dataset: {df.shape}\n")

# ----------------------------- #
# 0.1 — Check column dtypes
# ----------------------------- #
print("🔍 Checking data types...")
print(df.dtypes)
print("\n")

# ----------------------------- #
# 0.2 — Clean & fix data types
# ----------------------------- #

# Convert date columns (only if your dataset has them)
date_cols = [col for col in df.columns if "date" in col.lower()]

if date_cols:
    print(f"📅 Converting date columns: {date_cols}")
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
else:
    print("ℹ No date columns found.")

# Ensure category/type columns are string
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
print(f"🟦 Converting categorical columns to string: {categorical_cols}")

for col in categorical_cols:
    df[col] = df[col].astype(str)

# Ensure numeric columns are numeric
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
print(f"🟩 Numeric columns detected: {numeric_cols}")

# ----------------------------- #
# 0.3 — Save cleaned version
# ----------------------------- #

output_path = "data/final/customer360_powerbi_ready.csv"
df.to_csv(output_path, index=False)

print("\n🎉 Dataset cleaned & ready for Power BI!")
print(f"📁 Saved to: {output_path}")
print(f"📊 Final Shape: {df.shape}\n")
