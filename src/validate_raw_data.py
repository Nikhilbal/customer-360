import pandas as pd
import os

raw_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")

for file in os.listdir(raw_dir):
    if file.endswith(".csv") or file.endswith(".xlsx"):
        file_path = os.path.join(raw_dir, file)

        # Load CSV or Excel
        if file.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path, low_memory=False)

        print("\n---------------------------------------")
        print("File:", file)
        print("Shape:", df.shape)
        print("Columns:", list(df.columns)[:10])
        print("---------------------------------------")
