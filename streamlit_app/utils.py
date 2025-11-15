import pandas as pd
import os
import streamlit as st

DATA_PATH = "data/final/customer360_final_dataset.csv"
import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
            .main {
                background-color: #f9fafb;
            }
            h1, h2, h3 {
                color: #2c3e50;
                font-weight: 600;
            }
            .stButton button {
                background-color: #4CAF50 !important;
                color: white !important;
                border-radius: 8px !important;
                padding: 10px 20px !important;
            }
            .stAlert {
                font-size: 16px !important;
            }
        </style>
    """, unsafe_allow_html=True)


def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Dataset missing at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # ---- Fix Missing Required Columns ----
    if "frequency" not in df.columns:
        df["frequency"] = df.groupby("customer_id")["order_id"].transform("count")

    if "total_spent" not in df.columns:
        if "price" in df.columns:
            df["total_spent"] = df.groupby("customer_id")["price"].transform("sum")
        else:
            df["total_spent"] = df["frequency"] * 250  # fallback assumption

    if "recency" not in df.columns:
        df["recency"] = df.groupby("customer_id")["order_purchase_timestamp"].transform(
            lambda x: (pd.to_datetime(df["order_purchase_timestamp"]).max() - pd.to_datetime(x)).dt.days
        ) if "order_purchase_timestamp" in df.columns else 30

    if "product_category_name" not in df.columns:
        df["product_category_name"] = "Unknown"

    if "state_x" not in df.columns:
        if "customer_state" in df.columns:
            df["state_x"] = df["customer_state"]
        else:
            df["state_x"] = "Unknown"

    return df


def load_models():
    model_path = "streamlit_app/model/model.pkl"
    scaler_path = "streamlit_app/model/scaler.pkl"

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(
            f"🚨 Model/scaler missing.\nExpected:\n➡️ {model_path}\n➡️ {scaler_path}"
        )

    import pickle
    model = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
    
    return model, scaler
