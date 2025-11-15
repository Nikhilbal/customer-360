# streamlit_app/pages/page_churn_prediction.py

import os
import sys
import numpy as np
import streamlit as st
import plotly.express as px

# Allow importing utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import load_data, load_models


# ---------- Helper Function ----------

def format_inr(value):
    """Format number as Indian currency (INR)."""
    try:
        return f"₹{value:,.0f}" if value >= 1 else f"₹{value:.2f}"
    except:
        return value


# ---------- Main Page Function ----------

def show_churn_prediction(df=None):

    st.title("🔮 Churn Prediction & Customer Insights")

    # Load Data if Not Passed
    if df is None:
        df = load_data()

    if df is None or df.empty:
        st.error("❌ No dataset found. Please confirm your upload or file location.")
        return

    # Load trained model
    try:
        model, scaler = load_models()
    except Exception as e:
        st.error("❌ Could not load model files.")
        st.warning("Ensure the files `model.pkl` and `scaler.pkl` exist inside: `streamlit_app/model/`")
        st.code(f"Error: {e}")
        return

    st.markdown("Use this module to analyze churn behavior and interactively predict churn for a single customer.")

    st.markdown("---")

    # =========================
    # 📊 Churn Visualization
    # =========================

    st.subheader("📊 Current Customer Churn Distribution")

    churn_column = None
    for col in ["churn_flag", "Churn", "churn"]:
        if col in df.columns:
            churn_column = col
            break

    if churn_column:
        churn_data = df[churn_column].value_counts().reset_index()
        churn_data.columns = ["Status", "Count"]
        churn_data["Status"] = churn_data["Status"].map({1: "Churned", 0: "Active"})

        fig = px.pie(
            churn_data,
            values="Count",
            names="Status",
            title="Churn vs Active Customers"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠ No churn column detected in dataset — skipping chart.")

    st.markdown("---")

    # =========================
    # 🧠 Prediction Form
    # =========================

    st.subheader("🧠 Predict Individual Customer Churn")

    # Auto-detect input feature columns
    feature_cols = {
        "Recency": next((col for col in df.columns if "recency" in col.lower()), None),
        "Frequency": next((col for col in df.columns if "freq" in col.lower() or "orders" in col.lower()), None),
        "Total Spend": next((col for col in df.columns if "spent" in col.lower() or "payment" in col.lower()), None)
    }

    recency_val = int(df[feature_cols["Recency"]].median()) if feature_cols["Recency"] else 30
    freq_val = int(df[feature_cols["Frequency"]].median()) if feature_cols["Frequency"] else 3
    spend_val = int(df[feature_cols["Total Spend"]].median()) if feature_cols["Total Spend"] else 3000

    with st.form("churn_prediction_form"):

        recency = st.number_input("🕒 Days Since Last Purchase", min_value=0, value=recency_val)
        frequency = st.number_input("🛍️ Total Purchase Count", min_value=0, value=freq_val)
        total_spent = st.number_input("💰 Total Spending (INR)", min_value=0, value=spend_val)

        submitted = st.form_submit_button("Predict Churn 🔍")

    if submitted:

        input_row = np.array([[recency, frequency, total_spent]])

        try:
            scaled = scaler.transform(input_row)
            churn_probability = model.predict_proba(scaled)[0][1]
            prediction = model.predict(scaled)[0]
        except Exception as e:
            st.error(f"⚠ Prediction failed. Error: {e}")
            return

        st.markdown("---")

        if prediction == 1:
            st.error(f"⚠ High Risk — This customer is likely to churn.\n\n**Churn Probability:** `{churn_probability:.2%}`")
        else:
            st.success(f"🎉 Low Risk — This customer is unlikely to churn.\n\n**Churn Probability:** `{churn_probability:.2%}`")

        st.toast("Prediction Completed ✔")


    st.success("✅ Churn Prediction Module Ready")


