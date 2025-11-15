# streamlit_app/pages/page_overview.py

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data


# ------------------------ Helper Function ------------------------
def format_inr(value):
    """Format numbers as Indian Rupees."""
    try:
        return f"₹{value:,.0f}"
    except:
        return "₹0"


# ------------------------ Overview Page ------------------------
def show_overview(df):

    st.title("📊 Customer Overview Dashboard")

    # -------------------- Data Validation --------------------
    if df is None or df.empty:
        st.error("❌ No dataset found. Please load a valid CSV file.")
        return

    # -------------------- Detect Key Columns --------------------
    spend_candidates = ["total_spent", "payment_value", "Total_Spend", "price", "final_price"]
    spend_col = next((col for col in spend_candidates if col in df.columns), None)

    if not spend_col:
        st.warning("⚠ No revenue column found — spend-based charts disabled.")

    # Customer column detection (fixed logic)
    customer_candidates = ["customer_id", "CustomerID", "customer_unique_id"]
    customer_col = next((col for col in customer_candidates if col in df.columns), None)

    if not customer_col:
        st.error("❌ No customer ID column found.")
        return

    # -------------------- KPI Metrics --------------------
    total_customers = df[customer_col].nunique()
    total_revenue = df[spend_col].sum() if spend_col else 0
    avg_revenue = total_revenue / total_customers if total_customers > 0 else 0

    churn_candidates = [c for c in df.columns if "churn" in c.lower()]
    churn_col = churn_candidates[0] if churn_candidates else None
    churn_rate = (df[churn_col].mean() * 100) if churn_col and df[churn_col].dtype != "object" else None

    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Total Customers", f"{total_customers:,}")
    col2.metric("💰 Total Revenue", format_inr(total_revenue))
    col3.metric("📈 Avg Revenue per Customer", format_inr(avg_revenue))
    col4.metric("📉 Churn Rate", f"{churn_rate:.2f}%" if churn_rate else "Not Available")

    st.markdown("---")

    # -------------------- Segment Distribution --------------------
    if "segment_name" in df.columns:
        st.subheader("🧩 Customer Segment Distribution")
        seg = df.groupby("segment_name")[customer_col].nunique().reset_index()

        fig_seg = px.pie(
            seg,
            names="segment_name",
            values=customer_col,
            title="Customer Segments Overview",
            hole=0.4
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    # -------------------- Age Distribution --------------------
    if "Age" in df.columns:
        st.subheader("🎯 Age Distribution")

        fig_age = px.histogram(df, x="Age", nbins=20, title="Customer Age Frequency")
        st.plotly_chart(fig_age, use_container_width=True)

    # -------------------- Revenue Trend --------------------
    if "order_purchase_timestamp" in df.columns and spend_col:
        
        st.subheader("📆 Monthly Revenue Trend")

        # Convert dtype once (safe method)
        if not pd.api.types.is_datetime64_any_dtype(df["order_purchase_timestamp"]):
            df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")

        df["Month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

        trend = df.groupby("Month")[spend_col].sum().reset_index()

        fig_trend = px.line(
            trend,
            x="Month",
            y=spend_col,
            markers=True,
            title="Revenue Trend Over Time"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.success("✅ Dashboard Loaded Successfully!")


# -------- Streamlit entry point --------
def app():
    df = load_data()
    show_overview(df)
